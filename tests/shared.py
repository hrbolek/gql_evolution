import sqlalchemy
import asyncio
import pytest

async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    from DBs.DBDefinitions import BaseModel

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def prepare_demodata(async_session_maker):
    from DBs.DBFeeder import get_demodata
    from DBs.DBDefinitions import DisciplineModel, DisciplineSetModel, SummaryModel, ResultModel, NormModel

    data = get_demodata()

    from uoishelpers.feeders import ImportModels

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


async def createContext(asyncSessionMaker):
    from DBs.Dataloaders import createLoadersContext
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoadersContext(asyncSessionMaker),
    }