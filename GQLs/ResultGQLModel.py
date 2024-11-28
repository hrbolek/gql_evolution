import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
DisciplineGQLModel = typing.Annotated["DisciplineGQLModel", strawberry.lazy(".DisciplineGQLModel")]
SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]
NormGQLModel = typing.Annotated["NormGQLModel", strawberry.lazy(".NormGQLModel")]

@strawberry.type(description="Model representing a result of an examination")

class ResultGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "tested_person_id": lambda row: row.tested_person_id,
            "examiner_person_id": lambda row: row.examiner_person_id,
            "discipline_id": lambda row: row.discipline_id,
            "datetime": lambda row: row.datetime,
            "result": lambda row: row.result,
            "note": lambda row: row.note,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbaobject_id": lambda row: row.rbaobject_id,
        }

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ResultModel

    id: uuid.UUID = strawberry.field()
    tested_person_id: uuid.UUID = strawberry.field(description="ID of the tested person")
    examiner_person_id: uuid.UUID = strawberry.field(description="ID of the examiner person")
    discipline_id: uuid.UUID = strawberry.field(description="ID of the discipline")
    datetime: dt.datetime = strawberry.field(description="Date and time of the result")
    result: str = strawberry.field(description="Result of the test")
    note: typing.Optional[str] = strawberry.field(description="Additional note", default=None)
    lastchange: dt.datetime = strawberry.field(description="Last change")
    created: dt.datetime = strawberry.field(description="Created")
    createdby_id: uuid.UUID = strawberry.field(description="ID of the creator")
    changedby_id: uuid.UUID = strawberry.field(description="ID of the last changer")
    rbaobject_id: uuid.UUID = strawberry.field(description="ID of the RBA object")


    @strawberry.field(description="Returns an id of the tested person")
    async def tested_person(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[UserGQLModel]:
        result = await ResultGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns an id of the examiner person")
    async def examiner_person(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[UserGQLModel]:
        result = await ResultGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns a summaries for the result")
    async def summaries(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.List[SummaryGQLModel]:
        result = await SummaryGQLModel.load_with_loader(info=info, id=id)
        return result

@strawberry.field(description="Returns a result by id")
async def result_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ResultGQLModel]:
    result = await ResultGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of results")
async def result_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[ResultGQLModel]:
    loader = getLoadersFromInfo(info).results
    rows = await loader.page(skip, limit)
    return [ResultGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []
   
