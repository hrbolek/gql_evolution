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
            "effective_date": lambda row: row.effective_date,
            "expiration_date": lambda row: row.expiration_date,
            "point_range": lambda row: row.point_range,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbacobject_id": lambda row: row.rbacobject_id,
            "result_id": lambda row: row.result_id,
            "norm_id": lambda row: row.norm_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).SummaryModel
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).SummaryModel
    
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result is effective", default = None, permission_classes=[OnlyForAuthentized])
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result expires", default = None, permission_classes=[OnlyForAuthentized])
    point_range: typing.Optional[str] = strawberry.field(description="Range of points", default = None, permission_classes=[OnlyForAuthentized])
    result_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the result", default = None, permission_classes=[OnlyForAuthentized])
    norm_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the norm", default = None, permission_classes=[OnlyForAuthentized])

    @strawberry.field(description="Returns a discipline for the summary", permission_classes=[OnlyForAuthentized])
    async def disciplines(self, info: strawberry.types.Info) -> typing.List[DisciplineGQLModel]:
        from .DisciplineGQLModel import DisciplineGQLModel
        result = await DisciplineGQLModel.load_with_loader(info=info, id=self.discipline_id)
        return result

    @strawberry.field(description="Returns a discipline sets for the summary", permission_classes=[OnlyForAuthentized])
    async def sets(self, info: strawberry.types.Info) -> typing.List[DisciplineSetGQLModel]:
        from .DisciplineSetGQLModel import DisciplineSetGQLModel
        result = await DisciplineSetGQLModel.load_with_loader(info=info, id=self.disciplineSet_id)
        return result
    
    @strawberry.field(description="Returns result for the summary", permission_classes=[OnlyForAuthentized])
    async def result(self, info: strawberry.types.Info) -> typing.Optional[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await ResultGQLModel.load_with_loader(info=info, id=self.result_id)
        return result
    
    @strawberry.field(description="Returns a norm for the summary", permission_classes=[OnlyForAuthentized])
    async def norm(self, info: strawberry.types.Info) -> typing.Optional[NormGQLModel]:
        from .NormGQLModel import NormGQLModel
        result = await NormGQLModel.load_with_loader(info=info, id=self.norm_id)
        return result
    
@createInputs
@dataclasses.dataclass
class SummaryInputFilter:
    effective_date: dt.datetime
    expiration_date: dt.datetime
    point_range: str
    result_id: uuid.UUID
    norm_id: uuid.UUID
    
# Queries

@strawberry.field(description="Returns a sumamry by id", permission_classes=[OnlyForAuthentized])
async def summary_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[SummaryGQLModel]:
    result = await SummaryGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of summaries", permission_classes=[OnlyForAuthentized])
async def summary_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[SummaryGQLModel]:
    loader = SummaryGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [SummaryGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []

summary_page = strawberry.field(
        description="""Finds paged summaries""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[SummaryGQLModel](whereType=SummaryInputFilter)
        ) 

# Mutations

@strawberry.input(description="Definition of a summary used for insert")
class SummaryInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the summary", default=None)
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result is effective", default=None)
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result expires", default=None)
    point_range: typing.Optional[str] = strawberry.field(description="Range of points", default=None)
    result_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the result", default=None)
    norm_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the norm", default=None)

@strawberry.input(description="Definition of a summary used for update")
class SummaryUpdateGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the summary")
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result is effective", default=None)
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the result expires", default=None)
    point_range: typing.Optional[str] = strawberry.field(description="Range of points", default=None)
    result_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the result", default=None)
    norm_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the norm", default=None)

@strawberry.input(description="Definition of a summary used for delete")
class SummaryDeleteGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the summary")

#####

@strawberry.type(description="Result of a mutation for a summary")
class SummaryMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="ID of the summary", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK / FAIL)", default=None)

    @strawberry.field(description="Returns the summary")
    async def summary(self, info: strawberry.types.Info) -> typing.Optional[SummaryGQLModel]:
        summary = await SummaryGQLModel.load_with_loader(info=info, id=self.id)
        return summary

@strawberry.mutation(description="Creates a new summary", permission_classes=[OnlyForAuthentized])
async def summary_insert(self, info: strawberry.types.Info, summary: SummaryInsertGQLModel) -> typing.Union[SummaryGQLModel, InsertError[SummaryGQLModel]]:
    result = await Insert[SummaryGQLModel].DoItSafeWay(info=info, entity=summary)
    return result

@strawberry.mutation(description="Updates an existing summary", permission_classes=[OnlyForAuthentized])
async def summary_update(self, info: strawberry.types.Info, summary: SummaryUpdateGQLModel) -> typing.Union[SummaryGQLModel, UpdateError[SummaryGQLModel]]:
    result = await Update[SummaryGQLModel].DoItSafeWay(info=info, entity=summary)
    return result

@strawberry.mutation(description="Deletes a summary", permission_classes=[OnlyForAuthentized])
async def summary_delete(self, info: strawberry.types.Info, summary: SummaryDeleteGQLModel) -> typing.Optional[DeleteError[SummaryGQLModel]]:
    result = await Delete[SummaryGQLModel].DoItSafeWay(info=info, entity=summary)
    return result