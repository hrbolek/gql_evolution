import sqlalchemy
import asyncio
import pytest

# Prepare an in-memory SQLite database for testing
async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from DBs.DBDefinitions import BaseModel

    # Create an in-memory SQLite database
    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")  # Persistent SQLite option

    # Initialize database schema
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    # Create an async session maker
    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

# Populate the database with test data
async def prepare_demodata(async_session_maker):
    from DBs.DBFeeder import get_demodata
    from DBs.DBDefinitions import DisciplineModel, DisciplineSetModel, SummaryModel, ResultModel, NormModel
    from uoishelpers.feeders import ImportModels

    # Load test data
    data = get_demodata()

    # Import data into the database
    await ImportModels(
        async_session_maker,
        [
            NormModel,
            ResultModel,
            SummaryModel,
            DisciplineSetModel,
            DisciplineModel,           
        ],
        data,
    )

# Create a context containing the async session maker and data loaders
async def createContext(asyncSessionMaker):
    from DBs.Dataloaders import createLoadersContext

    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoadersContext(asyncSessionMaker),
    }
