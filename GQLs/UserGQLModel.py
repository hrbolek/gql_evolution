import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .baseGQLModel import BaseGQLModel

DisciplineGQLModel = typing.Annotated["DisciplineGQLModel", strawberry.lazy(".DisciplineGQLModel")]
DisciplineSetGQLModel = typing.Annotated["DisciplineSetGQLModel", strawberry.lazy(".DisciplineSetGQLModel")]
ResultGQLModel = typing.Annotated["ResultGQLModel", strawberry.lazy(".ResultGQLModel")]
SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]
NormGQLModel = typing.Annotated["NormGQLModel", strawberry.lazy(".NormGQLModel")]

@strawberry.type(description="Model representing a user")

class UserGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserModel
    
    id: uuid.UUID = strawberry.field()
    birthdate: dt.date = strawberry.field(description="Date of birth")
    male: bool = strawberry.field(description="User is male true")
    female: bool = strawberry.field(description="User is female if true")

    @strawberry.field(description="Returns disciplines for the user")
    async def disciplines(self, info: strawberry.types.Info,) -> typing.List[DisciplineGQLModel]:
        from .DisciplineGQLModel import DisciplineGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result
    
    @strawberry.field(description="Returns discipline sets for the user")
    async def sets(self,info: strawberry.types.Info,) -> typing.List[DisciplineSetGQLModel]:
        from .DisciplineSetGQLModel import DisciplineSetGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result

    @strawberry.field(description="Returns results of the user")
    async def results(self,info: strawberry.types.Info,) -> typing.List[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result
    
    @strawberry.field(description="Returns result template of the user")
    async def template(self,info: strawberry.types.Info,) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result
    
    @strawberry.field(description="Returns a norm for the user")
    async def norm(self,info: strawberry.types.Info,) -> typing.Optional[NormGQLModel]:
        from .NormGQLModel import NormGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result