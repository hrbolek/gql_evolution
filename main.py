import logging

# Configure logging format and level
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

# Store application context
appcontext = {}

# Async function to initialize the database engine
@asynccontextmanager
async def initEngine(app: FastAPI):
    from DBs import startEngine, ComposeConnectionString

    # Get database connection string
    connectionstring = ComposeConnectionString()

    # Start database engine
    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    # Store session maker in app context
    appcontext["asyncSessionMaker"] = asyncSessionMaker

    # Initialize database
    async def initwithmessage():
        await initDB(asyncSessionMaker)
        logging.info("DB initialized")
        print("DB initialized")

    await initwithmessage()

    logging.info("Engine started")
    print("Engine started")

    yield

# Create FastAPI app with database engine initialization
app = FastAPI(lifespan=initEngine)

logging.info("All initialization is done")

# Function to create data loader context
def context_getter():
    return createLoadersContext(appcontext["asyncSessionMaker"])

# Set up GraphQL router
graphql_app = GraphQLRouter(schema, context_getter=context_getter)
app.include_router(graphql_app, prefix="/gql")

# Serve Voyager UI for GraphQL exploration
@app.get("/voyager", response_class=FileResponse)
async def graphiql():
    realpath = os.path.realpath("./voyager.html")
    return realpath
