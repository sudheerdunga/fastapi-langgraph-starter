import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from contextlib import asynccontextmanager
from langgraph.checkpoint.memory import MemorySaver

from app.main import app
from app.providers.llm_factory import LLMFactory


class MockStreamingModel(FakeListChatModel):
    """Mock model that supports streaming and tool binding for unit tests."""

    def bind_tools(self, tools, **kwargs):
        return self


@pytest.fixture
def mock_llm(monkeypatch):
    """Mocks LLMFactory to return deterministic test responses."""
    model = MockStreamingModel(responses=["Mock AI response for testing."])
    monkeypatch.setattr(LLMFactory, "get_model", staticmethod(lambda **kwargs: model))
    return model


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def in_memory_checkpointer(monkeypatch):
    """Keeps test runs fast and in RAM without writing checkpoints.db to disk."""
    @asynccontextmanager
    async def mock_get_checkpointer():
        yield MemorySaver()
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.get_checkpointer",
        mock_get_checkpointer,
    )
