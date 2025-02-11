import aiohttp
import requests
import os
from contextlib import asynccontextmanager
from functools import cache
from fastapi import Request

@cache
def createProxy(url):
    assert url is not None, "createProxy(url) url is None"
    print(f"proxy for {url} created")

    # Defines a session class to store the authorization token
    class _Session:
        def __init__(self, authorizationToken):
            self.authorizationToken = authorizationToken

    # Defines a proxy class for making requests
    class Proxy:
        @asynccontextmanager
        async def Session(self, authorizationToken):
            result = self.connection(authorizationToken=authorizationToken)
            yield result

        @cache
        def connection(self, authorizationToken):
            return _Session(authorizationToken=authorizationToken)

        # Makes a POST request with a GraphQL query
        def post(self, query, variables={}):
            json = {"query": query, "variables": variables}
            response = requests.post(url=url, json=json)
            return response.json()

    return Proxy()

# Retrieves the user connection based on request headers or cookies
def get_ug_connection(request: Request):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    gqlproxy = createProxy(GQLUG_ENDPOINT_URL)

    authorizationToken = None
    authorizationBrearer = request.headers.get("authorization", None)

    # Gets the token from headers or cookies
    if authorizationBrearer is None:
        authorizationToken = request.cookies.get("authorization", None)
    else:
        [_, authorizationToken, *__] = authorizationBrearer.split(" ")

    return gqlproxy.connection(authorizationToken=authorizationToken)
