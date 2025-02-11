import pytest
import logging
import fastapi
import uvicorn
import pytest_asyncio
import pydantic
import time

from contextlib import contextmanager

# Define a Pydantic model for GraphQL requests
class Item(pydantic.BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

# Define the test scope for server fixtures
serversTestscope = "session"
# serversTestscope = "function"

# Start a FastAPI OAuth server for testing
def runOAuthServer(port, resolvers):
    mainapp = fastapi.FastAPI()
    
    @mainapp.post("/gql")
    async def post(item: Item):
        # Process request with available resolvers
        responses = (resolver(item) for resolver in resolvers)
        responses = (item for item in responses if item is not None)
        firstresponse = next(responses, None)
        return firstresponse

    logging.info(f"resolvers: {len(resolvers)}")
    uvicorn.run(mainapp, port=port)

# Context manager to start and stop the test OAuth server
@contextmanager
def runOauth(port, resolvers):
    from multiprocessing import Process
    
    _api_process = Process(target=runOAuthServer, daemon=True, kwargs={"port": port, "resolvers": resolvers})
    _api_process.start()
    time.sleep(5)  # Give the server time to start
    logging.info(f"OAuthServer started at {port}")
    
    yield _api_process  # Provide the server process

    # Stop the server process
    _api_process.terminate()
    _api_process.join()
    assert _api_process.is_alive() == False, "Server still alive :("
    logging.info(f"OAuthServer stopped at {port}")

import aiohttp
import pydantic

# Mock resolver for handling GraphQL queries
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

# List of resolvers to handle GraphQL queries
server_resolvers = [serveMe]

# Fixture to start the test server
@pytest.fixture(autouse=True, scope=serversTestscope)
def Server():
    serverport = 8125
    url = f"http://localhost:{serverport}/gql"

    # Async function to send requests to the test server
    async def client(query="", variables={}):
        payload = {"query": query, "variables": variables}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                assert resp.status == 200, resp
                accessjson = await resp.json()
        return accessjson

    with runOauth(serverport, resolvers=server_resolvers):
        yield client

NoRole_UG_Server = Server

@pytest_asyncio.fixture
async def Context():
    # Create an in-memory SQLite database for testing
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from DBs.DBDefinitions import BaseModel

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    # Enable demo data for testing
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("DEMODATA", "True")

    # Initialize the database with test data
    from DBs.DBFeeder import initDB
    await initDB(asyncSessionMaker=async_session_maker, filename="./systemdata.json")

    # Create data loaders for optimized database access
    from DBs.Dataloaders import createLoadersContext
    loadersContext = createLoadersContext(asyncSessionMaker=async_session_maker)

    # Mock request object for testing
    class Request:
        @property
        def cookies(self):
            return {}

        @property
        def headers(self):
            return {}

    # Assemble the test context
    context_ = {
        **loadersContext,
        "request": Request(),
    }

    logging.info(f"Context created")
    return context_

# Fixture to execute GraphQL queries in tests
@pytest.fixture
def SchemaExecutor(Context):
    # Set environment variable for GraphQL endpoint
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8125/gql")

    from GQLs.__init__ import schema

    # Function to execute queries using the schema
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=Context)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value

    return Execute

SchemaExecutorDemo = SchemaExecutor
