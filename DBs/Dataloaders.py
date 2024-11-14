from uoishelpers.dataloaders import createLoadersAuto
from DBs.baseDBModel import BaseModel

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoadersAuto(asyncSessionMaker, BaseModel=BaseModel)
    }