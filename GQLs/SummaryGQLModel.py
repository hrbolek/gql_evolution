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
NormGQLModel = typing.Annotated["NormGQLModel", strawberry.lazy(".NormGQLModel")]

@strawberry.type(description="Model representing a summary of results for a person or a group of persons")

class SummaryGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "discipline_id": lambda row: row.discipline_id,
            "discipline_set_id": lambda row: row.discipline_set_id,
            "effective_date": lambda row: row.effective_date,
            "expiration_date": lambda row: row.expiration_date,
            "point_range": lambda row: row.point_range,
            "point_type": lambda row: row.point_type,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbaobject_id": lambda row: row.rbaobject_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).SummaryModel
    
    id: uuid.UUID = strawberry.field()
    effective_date: dt.datetime = strawberry.field(description="Date when the result is effective")
    expiration_date: dt.datetime = strawberry.field(description="Date when the result expires")
    point_range: str = strawberry.field(description="Range of points")
    point_type: str = strawberry.field(description="Type of points")
    lastchange: dt.datetime = strawberry.field(description="Last change")
    created: dt.datetime = strawberry.field(description="Created")
    createdby_id: uuid.UUID = strawberry.field(description="ID of the creator")
    changedby_id: uuid.UUID = strawberry.field(description="ID of the last changer")
    rbaobject_id: uuid.UUID = strawberry.field(description="ID of the RBA object")

    @strawberry.field(description="Returns a discipline for the summary")
    async def disciplines(self, info: strawberry.types.Info) -> typing.List[DisciplineGQLModel]:
        from .DisciplineGQLModel import DisciplineGQLModel
        result = await DisciplineGQLModel.load_with_loader(info=info, id=self.discipline_id)
        return result

    @strawberry.field(description="Returns a discipline sets for the summary")
    async def sets(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.List[DisciplineSetGQLModel]:
        result = await DisciplineSetGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns result for the summary")
    async def result(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await ResultGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns a norm for the summary")
    async def norm(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[NormGQLModel]:
        from .NormGQLModel import NormGQLModel
        result = await NormGQLModel.load_with_loader(info=info, id=id)
        return result

@strawberry.field(description="Returns a sumamry by id")
async def summary_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[SummaryGQLModel]:
    result = await SummaryGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of summaries")
async def summary_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[SummaryGQLModel]:
    loader = getLoadersFromInfo(info).summaries
    rows = await loader.page(skip, limit)
    return [SummaryGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []