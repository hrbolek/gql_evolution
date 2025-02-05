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
    class _Session:
        def __init__(self, authorizationToken):
            self.authorizationToken = authorizationToken
            
    class Proxy:
        @asynccontextmanager
        async def Session(self, authorizationToken):
            result = self.connection(authorizationToken=authorizationToken)
            yield result
            pass
            
        @cache
        def connection(self, authorizationToken):
            result = _Session(authorizationToken=authorizationToken)
            return result
        
        def post(self, query, variables={}):
            json = {"query": query, "variables": variables}
            response = requests.post(url=url, json=json)
            result = response.json()
            return result

    return Proxy()

def get_ug_connection(request: Request):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    gqlproxy = createProxy(GQLUG_ENDPOINT_URL)

    authorizationToken = None
    authorizationBrearer = request.headers.get("authorization", None)
    if authorizationBrearer is None:
        authorizationToken = request.cookies.get("authorization", None)
    else:
        [_, authorizationToken, *__] = authorizationBrearer.split(" ")

    return gqlproxy.connection(authorizationToken=authorizationToken)