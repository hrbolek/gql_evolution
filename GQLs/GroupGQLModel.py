import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

DisciplineSetGQLModel = typing.Annotated["DisciplineSetGQLModel", strawberry.lazy(".DisciplineSetGQLModel")]
ResultGQLModel = typing.Annotated["ResultGQLModel", strawberry.lazy(".ResultGQLModel")]
SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]
NormGQLModel = typing.Annotated["NormGQLModel", strawberry.lazy(".NormGQLModel")]

@strawberry.type(description="Model representing a group")
class GroupGQLModel(BaseGQLModel):

    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).GroupModel

    @strawberry.field(description="Returns discipline sets for the group")
    async def sets(self, info: strawberry.types.Info) -> typing.List[DisciplineSetGQLModel]:
        from .DisciplineSetGQLModel import DisciplineSetGQLModel
        result = await GroupGQLModel.load_with_loader(info=info)
        return result
    
    @strawberry.field(description="Returns results of the group")
    async def results(self, info: strawberry.types.Info) -> typing.List[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await GroupGQLModel.load_with_loader(info=info)
        return result
    
    @strawberry.field(description="Returns summary of the group")
    async def summary(self, info: strawberry.types.Info) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await GroupGQLModel.load_with_loader(info=info)
        return result

    @strawberry.field(description="Returns a norm for the group")
    async def norm(self,info: strawberry.types.Info,) -> typing.Optional[NormGQLModel]:
        from .NormGQLModel import NormGQLModel
        result = await GroupGQLModel.load_with_loader(info=info)
        return result