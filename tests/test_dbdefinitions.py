import pytest, os
from uuid import UUID
from unittest.mock import patch, MagicMock
from fastapi import Request
from .shared import prepare_demodata, prepare_in_memory_sqllite
from DBs.uuid import uuid
from DBs.gql_ug_proxy import createProxy, get_ug_connection

# Test async function for user table data
@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    # data = get_demodata()

# Test creating a connection string
def test_connection_string():
    from DBs.__init__ import ComposeConnectionString
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString

# Test creating a UUID column
def test_connection_uuidcolumn():
    from DBs.DBDefinitions import UUIDColumn
    col = UUIDColumn(name="name")

    assert col is not None

# Test UUID generation
def test_uuid_generation():
    generated_uuid = uuid()
    assert isinstance(generated_uuid, UUID), "UUID must be an instance of UUID class"
    assert len(str(generated_uuid)) == 36, "UUID must be 36 characters long including dashes"

# Test UUID uniqueness
def test_uuid_uniqueness():
    uuid1 = uuid()
    uuid2 = uuid()
    assert uuid1 != uuid2, "UUIDs must be unique"

# Mocked FastAPI Request object with authorization
@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.headers = {"authorization": "Bearer mock_token"}
    request.cookies = {}
    return request

# Test proxy instance creation
def test_create_proxy():
    proxy = createProxy("http://mock-url.com")
    assert proxy is not None, "Failed to create proxy"
    assert hasattr(proxy, "Session"), "Proxy must contain a Session method"
    assert hasattr(proxy, "post"), "Proxy must contain a post method"

# Test calling the post method in proxy
def test_proxy_post_request():
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"data": "mock_response"}
        proxy = createProxy("http://mock-url.com")
        response = proxy.post("query { test }", {"param": "value"})

        assert response == {"data": "mock_response"}, "Proxy post request did not return the correct response"
        mock_post.assert_called_once_with(url="http://mock-url.com", json={"query": "query { test }", "variables": {"param": "value"}})

# Test retrieving UG GraphQL endpoint connection
@patch.dict(os.environ, {"GQLUG_ENDPOINT_URL": "http://mock-url.com"})
def test_get_ug_connection(mock_request):
    connection = get_ug_connection(mock_request)
    
    assert connection is not None, "Failed to get UG connection"
    assert connection.authorizationToken == "mock_token", "Authorization token is not passed correctly"

# Test async function for starting database engine
@pytest.mark.asyncio
async def test_table_start_engine():
    from DBs.__init__ import startEngine
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
