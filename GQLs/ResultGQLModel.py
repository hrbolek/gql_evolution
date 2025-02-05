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

from .BaseGQLModel import BaseGQLModel

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]

@strawberry.type(description="Model representing a result of an examination")
class ResultGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "tested_person_id": lambda row: row.tested_person_id,
            "examiner_person_id": lambda row: row.examiner_person_id,
            "evaluation_date": lambda row: row.evaluation_date,
            "result": lambda row: row.result,
            "note": lambda row: row.note,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbacobject_id": lambda row: row.rbacobject_id,
        }

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ResultModel
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ResultModel

    tested_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the tested person", default = None, permission_classes=[OnlyForAuthentized])
    examiner_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the examiner person", default = None, permission_classes=[OnlyForAuthentized])
    evaluation_date: typing.Optional[dt.datetime] = strawberry.field(description="Date and time of the result", default = None, permission_classes=[OnlyForAuthentized])
    result: typing.Optional[str] = strawberry.field(description="Result of the test", default = None, permission_classes=[OnlyForAuthentized])
    note: typing.Optional[str] = strawberry.field(description="Additional note", default=None, permission_classes=[OnlyForAuthentized])

    @strawberry.field(description="Returns an id of the tested person", permission_classes=[OnlyForAuthentized])
    async def tested_person(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[UserGQLModel]:
        from .UserGQLModel import UserGQLModel
        result = await ResultGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns an id of the examiner person", permission_classes=[OnlyForAuthentized])
    async def examiner_person(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[UserGQLModel]:
        from .UserGQLModel import UserGQLModel
        result = await ResultGQLModel.load_with_loader(info=info, id=id)
        return result
    
    @strawberry.field(description="Returns a summaries for the result", permission_classes=[OnlyForAuthentized])
    async def summaries(self, info: strawberry.types.Info) -> typing.List[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=self.summary_id)
        return result
    
@createInputs
@dataclasses.dataclass
class ResultInputFilter:
    tested_person_id: uuid.UUID
    examiner_person_id: uuid.UUID
    evaluation_date: dt.datetime
    result: str
    note: str

# Queries

@strawberry.field(description="Returns a result by id", permission_classes=[OnlyForAuthentized])
async def result_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ResultGQLModel]:
    result = await ResultGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of results", permission_classes=[OnlyForAuthentized])
async def result_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[ResultGQLModel]:
    loader = ResultGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [ResultGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []

result_page = strawberry.field(
        description="""Finds paged results""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ResultGQLModel](whereType=ResultInputFilter)
        ) 
   
# Mutations

@strawberry.input(description="Definition of a result used for insert")
class ResultInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the result", default=None)
    tested_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the tested person", default=None)
    examiner_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the examiner person", default=None)
    evaluation_date: typing.Optional[dt.datetime] = strawberry.field(description="Date and time of the result", default=None)
    result: typing.Optional[str] = strawberry.field(description="Result of the test", default=None)
    note: typing.Optional[str] = strawberry.field(description="Additional note", default=None)
    createdby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the user who created this record", default=None)

@strawberry.input(description="Definition of a result used for update")
class ResultUpdateGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the result")
    tested_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the tested person", default=None)
    examiner_person_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the examiner person", default=None)
    evaluation_date: typing.Optional[dt.datetime] = strawberry.field(description="Date and time of the result", default=None)
    result: typing.Optional[str] = strawberry.field(description="Result of the test", default=None)
    note: typing.Optional[str] = strawberry.field(description="Additional note", default=None)
    changedby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the user who last modified this record", default=None)

@strawberry.input(description="Definition of a result used for delete")
class ResultDeleteGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the result")

#####

@strawberry.type(description="Result of a mutation for a result")
class ResultMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="ID of the result", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK / FAIL)", default=None)

    @strawberry.field(description="Returns the result")
    async def result(self, info: strawberry.types.Info) -> typing.Union[ResultGQLModel, None]:
        result = await ResultGQLModel.load_with_loader(info=info, id=self.id)
        return result

@strawberry.mutation(description="Creates a new result", permission_classes=[OnlyForAuthentized])
async def result_insert(self, info: strawberry.types.Info, result: ResultInsertGQLModel) -> typing.Union[ResultGQLModel, InsertError[ResultGQLModel]]:
    result = await Insert[ResultGQLModel].DoItSafeWay(info=info, entity=result)
    return result

@strawberry.mutation(description="Updates an existing result", permission_classes=[OnlyForAuthentized])
async def result_update(self, info: strawberry.types.Info, result: ResultUpdateGQLModel) -> typing.Union[ResultGQLModel, UpdateError[ResultGQLModel]]:
    result = await Update[ResultGQLModel].DoItSafeWay(info=info, entity=result)
    return result

@strawberry.mutation(description="Deletes a result", permission_classes=[OnlyForAuthentized])
async def result_delete(self, info: strawberry.types.Info, result: ResultDeleteGQLModel) -> typing.Optional[DeleteError[ResultGQLModel]]:
    result = await Delete[ResultGQLModel].DoItSafeWay(info=info, entity=result)
    return result
