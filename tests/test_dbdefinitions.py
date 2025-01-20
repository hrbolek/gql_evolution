import pytest
from .shared import prepare_demodata, prepare_in_memory_sqllite

@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    # data = get_demodata()

def test_connection_string():
    from DBs.__init__ import ComposeConnectionString
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


def test_connection_uuidcolumn():
    from DBs.DBDefinitions import UUIDColumn
    col = UUIDColumn(name="name")

    assert col is not None


@pytest.mark.asyncio
async def test_table_start_engine():
    from DBs.__init__ import startEngine
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None