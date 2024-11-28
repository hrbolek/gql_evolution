import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

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
    male: bool = strawberry.field(description="User is male true")
    female: bool = strawberry.field(description="User is female if true")

    @strawberry.field(description="Returns result of the user")
    async def result(self,info: strawberry.types.Info,) -> typing.Optional[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result