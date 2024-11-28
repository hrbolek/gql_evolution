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

@strawberry.type(description="Model representing a single discipline")

class DisciplineGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "name": lambda row: row.name,
            "nameEn": lambda row: row.nameEn,
            "description": lambda row: row.description,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbaobject_id": lambda row: row.rbaobject_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DisciplineModel
    
    id: uuid.UUID = strawberry.field()
    name: str = strawberry.field(description="Name of the discipline")
    nameEn: str = strawberry.field(description="Name of the discipline in English")
    description: str = strawberry.field(description="Description of the discipline")
    lastchange: dt.datetime = strawberry.field(description="Last change")
    created: dt.datetime = strawberry.field(description="Created")
    createdby_id: uuid.UUID = strawberry.field(description="ID of the creator")
    changedby_id: uuid.UUID = strawberry.field(description="ID of the last changer")
    rbaobject_id: uuid.UUID = strawberry.field(description="ID of the RBA object")
    
    @strawberry.field(description="Returns a summary of the discipline")
    async def summary(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await DisciplineGQLModel.load_with_loader(info=info, id=id)
        return result

@strawberry.field(description="Returns a discpline by id")
async def discipline_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[DisciplineGQLModel]:
    result = await DisciplineGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of disciplines")
async def discipline_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[DisciplineGQLModel]:
    loader = getLoadersFromInfo(info).disciplines
    rows = await loader.page(skip, limit)
    return [DisciplineGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []