async function streamChat({ message, threadId, tools }: { message: string; threadId: string; tools?: string[] }) {
    const response = await fetch("http://localhost:8000/api/v1/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, thread_id: threadId, tools }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        let currentEvent = "";
        for (const line of lines) {
            if (line.startsWith("event: ")) {
                currentEvent = line.replace("event: ", "").trim();
            } else if (line.startsWith("data: ")) {
                const data = JSON.parse(line.replace("data: ", ""));

                if (currentEvent === "token") {
                    // Append streaming token to UI
                    console.log("Token delta:", data.delta);
                } else if (currentEvent === "tool_start") {
                    // Show spinner or badge: "⚙️ Calling tool: calculate..."
                    console.log("Tool executing:", data.tool, data.input);
                } else if (currentEvent === "tool_end") {
                    // Show tool result
                    console.log("Tool finished:", data.output);
                } else if (currentEvent === "done") {
                    console.log("Stream finished!");
                }
            }
        }
    }
}
