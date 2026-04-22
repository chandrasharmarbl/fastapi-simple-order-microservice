import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session


@pytest.mark.asyncio
async def test_get_db_session_yields_session():
    # FastAPI Depends generators can be tested by iterating over them
    generator = get_db_session()
    
    # The first yield should give us an AsyncSession
    session = await anext(generator)
    assert isinstance(session, AsyncSession)
    
    # The next iteration should raise StopAsyncIteration,
    # meaning the dependency generator finished (which triggers the finally block to close the session)
    with pytest.raises(StopAsyncIteration):
        await anext(generator)
