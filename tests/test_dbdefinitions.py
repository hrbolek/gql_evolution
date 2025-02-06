import pytest, os
from uuid import UUID
from unittest.mock import patch, MagicMock
from fastapi import Request
from .shared import prepare_demodata, prepare_in_memory_sqllite
from DBs.uuid import uuid
from DBs.gql_ug_proxy import createProxy, get_ug_connection

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

def test_uuid_generation():
    """Testuje, zda funkce uuid vygeneruje platné UUID."""
    generated_uuid = uuid()
    assert isinstance(generated_uuid, UUID), "UUID musí být instance třídy UUID"
    assert len(str(generated_uuid)) == 36, "UUID musí mít 36 znaků včetně pomlček"

def test_uuid_uniqueness():
    """Testuje, zda dvě různá volání uuid() vrátí různé hodnoty."""
    uuid1 = uuid()
    uuid2 = uuid()
    assert uuid1 != uuid2, "UUID musí být unikátní"

@pytest.fixture
def mock_request():
    """Mockovaný objekt FastAPI Request s autorizací."""
    request = MagicMock(spec=Request)
    request.headers = {"authorization": "Bearer mock_token"}
    request.cookies = {}
    return request

def test_create_proxy():
    """Testuje vytvoření proxy instance."""
    proxy = createProxy("http://mock-url.com")
    assert proxy is not None, "Proxy se nepodařilo vytvořit"
    assert hasattr(proxy, "Session"), "Proxy musí obsahovat Session metodu"
    assert hasattr(proxy, "post"), "Proxy musí obsahovat post metodu"

def test_proxy_post_request():
    """Testuje volání metody post v proxy."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"data": "mock_response"}
        proxy = createProxy("http://mock-url.com")
        response = proxy.post("query { test }", {"param": "value"})

        assert response == {"data": "mock_response"}, "Proxy post request nevrátil správnou odpověď"
        mock_post.assert_called_once_with(url="http://mock-url.com", json={"query": "query { test }", "variables": {"param": "value"}})

@patch.dict(os.environ, {"GQLUG_ENDPOINT_URL": "http://mock-url.com"})
def test_get_ug_connection(mock_request):
    """Testuje získání připojení k UG GraphQL endpointu."""
    connection = get_ug_connection(mock_request)
    
    assert connection is not None, "Nepodařilo se získat UG připojení"
    assert connection.authorizationToken == "mock_token", "Authorization token není správně předán"

@pytest.mark.asyncio
async def test_table_start_engine():
    from DBs.__init__ import startEngine
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None