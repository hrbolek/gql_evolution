from uoishelpers.dataloaders import createLoadersAuto
from DBs.BaseDBModel import BaseModel

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoadersAuto(asyncSessionMaker, BaseModel=BaseModel)
    }