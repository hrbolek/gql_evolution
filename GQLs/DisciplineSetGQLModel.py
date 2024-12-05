import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]

@strawberry.type(description="Model representing a set of discipline")
class DisciplineSetGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "name": lambda row: row.name,
            "name_en": lambda row: row.name_en,
            "description": lambda row: row.description,
            "minimum_points": lambda row: row.minimum_points,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbacobject_id": lambda row: row.rbacobject_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DisciplineSetModel
    
    name: typing.Optional[str] = strawberry.field(description="Name of the discipline set", default = None)
    name_en: typing.Optional[str] = strawberry.field(description="Name of the discipline set in English", default = None)
    description: typing.Optional[str] = strawberry.field(description="Description of the discipline set", default = None)
    minimum_points: typing.Optional[int] = strawberry.field(description="Minimum points to pass the discipline set", default = None)
    
    @strawberry.field(description="Returns a summary of the discipline set")
    async def summary(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=id)
        return result

@strawberry.field(description="Returns a discipline set by id")
async def discipline_set_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[DisciplineSetGQLModel]:
    result = await DisciplineSetGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of discipline sets")
async def discipline_set_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[DisciplineSetGQLModel]:
    loader = DisciplineSetGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [DisciplineSetGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []