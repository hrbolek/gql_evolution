from uoishelpers.dataloaders import createLoadersAuto
from DBs.BaseDBModel import BaseModel

# Creates a context with data loaders using the provided async session maker
def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoadersAuto(asyncSessionMaker, BaseModel=BaseModel)
    }