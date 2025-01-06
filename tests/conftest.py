import pytest
import logging
import fastapi
import uvicorn
import pytest_asyncio
import pydantic
import time

from contextlib import contextmanager

class Item(pydantic.BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

serversTestscope = "session"
# serversTestscope = "function"

def runOAuthServer(port, resolvers):
    mainapp = fastapi.FastAPI()
    @mainapp.post("/gql")
    async def post(item: Item):
        responses = (resolver(item) for resolver in resolvers)
        responses = (item for item in responses if item is not None)
        firstresponse = next(responses, None)
        return firstresponse
        # return {"hello": "world", "resolvers": len(resolvers), "item": item}
    logging.info(f"resolvers: {len(resolvers)}")
    uvicorn.run(mainapp, port=port)

@contextmanager
def runOauth(port, resolvers):
    from multiprocessing import Process
    
    _api_process = Process(target=runOAuthServer, daemon=True, kwargs={"port": port, "resolvers": resolvers})
    _api_process.start()
    # time.sleep(2)
    logging.info(f"OAuthServer started at {port}")
    
    yield _api_process
    _api_process.terminate()
    _api_process.join()
    assert _api_process.is_alive() == False, "Server still alive :("
    logging.info(f"OAuthServer stopped at {port}")

# @pytest.fixture(scope=serversTestscope)
# def UserInfoServer(monkeypatch, AdminUser):
#     UserInfoServerPort = 8126
#     monkeypatch.setenv("JWTRESOLVEUSERPATHURL", f"http://localhost:{UserInfoServerPort}/oauth/userinfo") #/oauth/publickey
#     logging.info(f"JWTRESOLVEUSERPATHURL set to `http://localhost:{UserInfoServerPort}/oauth/userinfo`")
#     yield from runUserInfo(UserInfoServerPort, AdminUser)

# @pytest.fixture(scope="session")

import aiohttp
import pydantic

def serveMe(item: Item):
    logging.info(f"serveMe {item}")
    if "me {" in item.query:
        result = {
            "data": {
                "me": {
                    "id": "51d101a0-81f1-44ca-8366-6cf51432e8d6",
                    "roles": [
                        {
                            "roletype": {"name": "administrátor"}
                        }
                    ]
                }
            }
        }
        
    else:
        result = None
    return result

server_resolvers = [
    serveMe
]

@pytest.fixture(autouse=True, scope=serversTestscope)
def Server():
    serverport = 8125

    url = f"http://localhost:{serverport}/gql"
    async def client(query="", variables={}):
        payload = {
            "query": query,
            "variables": variables
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                assert resp.status == 200, resp
                accessjson = await resp.json()
        return accessjson

    with runOauth(serverport, resolvers=server_resolvers):
        yield client

NoRole_UG_Server = Server

# @pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
# async def AccessToken(Server):
#     token = await Server()
#     logging.info(f"have token {token}")
#     yield token
#     logging.info(f"expiring token {token} ")

# @pytest.fixture
# def LoadersContext(SQLite):
#     from src.Dataloaders import createLoadersContext
#     context = createLoadersContext(SQLite)
#     return context

# @pytest.fixture
# def Context(AdminUser, SQLite, LoadersContext, Request):
#     # from src.gql_ug_proxy import get_ug_connection
    
#     Async_Session_Maker = SQLite
#     return {
#         **LoadersContext,
#         "request": Request,
#         "": Async_Session_Maker,
#         "user": AdminUser,
#         "x": "",
#         # "ug_connection": get_ug_connection
#     }

@pytest_asyncio.fixture
async def Context():
    # async_session_maker
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

    # fill data
    # patch DEMODATA to True
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("DEMODATA", "True")

    from DBs.DBFeeder import initDB
    await initDB(asyncSessionMaker=async_session_maker, filename="./systemdata.json")
    # context
    from DBs.Dataloaders import createLoadersContext
    loadersContext = createLoadersContext(asyncSessionMaker=async_session_maker)
    # ...

    class Request:
        @property
        def cookies(self):
            return {}
        @property
        def headers(self):
            return {}
        
    context_ = {
        **loadersContext,
        "request": Request(),
        # "": async_session_maker,
        # "user": AdminUser,
        # "x": "",
        # "ug_connection": get_ug_connection
    }
    # class _Info():
    #     @property
    #     def context(self):
    #         context = context_
    #         # context["request"] = Request
    #         return context

    # return _Info()
    logging.info(f"Context created")
    return context_

@pytest.fixture
def SchemaExecutor(Context):
    # GQLUG_ENDPOINT_URL
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8125/gql")

    from GQLs.__init__ import schema
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=Context)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value
    return Execute

SchemaExecutorDemo = SchemaExecutor