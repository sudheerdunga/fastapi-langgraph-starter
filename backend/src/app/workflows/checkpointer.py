from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.core.config import get_settings


@asynccontextmanager
async def get_checkpointer() -> AsyncGenerator[AsyncSqliteSaver, None]:
    """Provides an async SQLite checkpointer for persisting graph sessions.
    
    The database path is read from settings (e.g. checkpoints.db).
    """
    settings = get_settings()
    async with AsyncSqliteSaver.from_conn_string(settings.CHECKPOINT_DB_PATH) as saver:
        yield saver