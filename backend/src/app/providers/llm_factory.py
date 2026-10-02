from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import Settings, get_settings


class LLMFactory:
    """Factory to dynamically instantiate chat models based on provider."""

    @staticmethod
    def get_model(
        provider: str | None = None,
        model_name: str | None = None,
        temperature: float | None = None,
        streaming: bool = True,
        **kwargs: Any,
    ) -> BaseChatModel:
        settings: Settings = get_settings()

        resolved_provider = (provider or settings.DEFAULT_MODEL_PROVIDER).lower()
        resolved_model = model_name or settings.DEFAULT_MODEL_NAME
        resolved_temp = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE

        match resolved_provider:
            case "anthropic":
                from langchain_anthropic import ChatAnthropic

                if not settings.ANTHROPIC_API_KEY:
                    raise ValueError(
                        "ANTHROPIC_API_KEY is not set. Please add it to your .env file."
                    )
                return ChatAnthropic(
                    model=resolved_model,
                    temperature=resolved_temp,
                    api_key=settings.ANTHROPIC_API_KEY,
                    streaming=streaming,
                    **kwargs,
                )

            case "google":
                from langchain_google_genai import ChatGoogleGenerativeAI

                if not settings.GOOGLE_API_KEY:
                    raise ValueError(
                        "GOOGLE_API_KEY is not set. Please add it to your .env file."
                    )
                return ChatGoogleGenerativeAI(
                    model=resolved_model,
                    temperature=resolved_temp,
                    api_key=settings.GOOGLE_API_KEY,
                    streaming=streaming,
                    **kwargs,
                )

            case "ollama":
                from langchain_ollama import ChatOllama

                return ChatOllama(
                    model=resolved_model,
                    temperature=resolved_temp,
                    base_url=settings.OLLAMA_BASE_URL,
                    **kwargs,
                )

            case _:
                raise ValueError(
                    f"Unsupported provider: '{resolved_provider}'. "
                    f"Supported providers are: 'anthropic', 'google', 'ollama'."
                )
