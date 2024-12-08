import logging
logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(message)s', level=logging.DEBUG, datefmt='%Y-%m-%dT%I:%M:%S')

import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.responses import FileResponse
from DBs.Dataloaders import createLoadersContext
from DBs.DBFeeder import initDB

from GQLs import schema

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    from DBs import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker
    async def initwithmessage():
        await initDB(asyncSessionMaker)
        logging.info("DB initialized")
        print("DB initialized")
    #task = asyncio.create_task(initwithmessage())
    await initwithmessage()

    logging.info("engine started")
    print("engine started")
    
    yield

app = FastAPI(lifespan=initEngine)

logging.info("All initialization is done ")

@app.get('/hello')
def hello():
   return {'hello': 'world'}

def context_getter():
    return createLoadersContext(appcontext["asyncSessionMaker"])

graphql_app = GraphQLRouter(schema, context_getter=context_getter)

app.include_router(graphql_app, prefix="/gql", )

@app.get("/voyager", response_class=FileResponse)
async def graphiql():
    realpath = os.path.realpath("./voyager.html")
    return realpath