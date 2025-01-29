import strawberry
import uuid
import typing
import datetime as dt
import dataclasses

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)

from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

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
    
    male: typing.Optional[bool] = strawberry.field(description="User is male true", default = None)
    female: typing.Optional[bool] = strawberry.field(description="User is female if true", default = None)

    @strawberry.field(description="Returns result of the user")
    async def result(self,info: strawberry.types.Info,) -> typing.Optional[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await UserGQLModel.load_with_loader(info=info)
        return result