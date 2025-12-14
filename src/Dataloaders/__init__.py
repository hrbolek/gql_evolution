# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from src.DBDefinitions import (
    EventModel,
    EventInvitationModel,
    ProjectModel,
    FinanceModel,
    MilestoneModel,

)

from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel

    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    ProjectModel: IDLoader[src.DBDefinitions.ProjectModel] = None
    FinanceModel: IDLoader[src.DBDefinitions.FinanceModel] = None
    MilestoneModel: IDLoader[src.DBDefinitions.MilestoneModel] = None

    def __init__(self, session):
        super().__init__(session)

        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.ProjectModel = self.get(ProjectModel)
        self.FinanceModel = self.get(FinanceModel)
        self.MilestoneModel = self.get(MilestoneModel)
        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
