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

SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]

@strawberry.type(description="Model representing a single discipline")
class DisciplineGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "name": lambda row: row.name,
            "name_en": lambda row: row.name_en,
            "description": lambda row: row.description,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbacobject_id": lambda row: row.rbacobject_id,
            "summary_id": lambda row: row.summary_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DisciplineModel
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).DisciplineModel

    name: typing.Optional[str] = strawberry.field(description="Name of the discipline", default=None, permission_classes=[OnlyForAuthentized])
    name_en: typing.Optional[str] = strawberry.field(description="Name of the discipline in English", default=None, permission_classes=[OnlyForAuthentized])
    description: typing.Optional[str] = strawberry.field(description="Description of the discipline", default=None, permission_classes=[OnlyForAuthentized])
    summary_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the summary", default=None, permission_classes=[OnlyForAuthentized])
    
    @strawberry.field(description="Returns a summary of the discipline", permission_classes=[OnlyForAuthentized])
    async def summary(self, info: strawberry.types.Info) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=self.summary_id)
        return result
    
@createInputs
@dataclasses.dataclass
class DisciplineInputFilter:
    name: str
    name_en: str
    description: str
    summary_id: uuid.UUID

# Queries

@strawberry.field(description="Returns a discipline by id", permission_classes=[OnlyForAuthentized])
async def discipline_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[DisciplineGQLModel]:
    result = await DisciplineGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of disciplines", permission_classes=[OnlyForAuthentized])
async def discipline_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[DisciplineGQLModel]:
    loader = DisciplineGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [DisciplineGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []

discipline_page = strawberry.field(
        description="""Finds paged disciplines""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[DisciplineGQLModel](whereType=DisciplineInputFilter)
        )    

# Mutations

@strawberry.input(description="Definition of a discipline used for insert")
class DisciplineInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the discipline", default=None)
    name: typing.Optional[str] = strawberry.field(description="Name of the discipline", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="Name of the discipline in English", default=None)
    description: typing.Optional[str] = strawberry.field(description="Description of the discipline", default=None)
    summary_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the summary", default=None)

@strawberry.input(description="Definition of a discipline used for update")
class DisciplineUpdateGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the discipline")
    name: typing.Optional[str] = strawberry.field(description="Name of the discipline", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="Name of the discipline in English", default=None)
    description: typing.Optional[str] = strawberry.field(description="Description of the discipline", default=None)
    summary_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the summary", default=None)

@strawberry.input(description="Definition of a discipline used for delete")
class DisciplineDeleteGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the discipline")

#####

@strawberry.type(description="Result of a mutation for a discipline")
class DisciplineMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="ID of the discipline", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK / FAIL)", default=None)

    @strawberry.field(description="Returns the discipline")
    async def discipline(self, info: strawberry.types.Info) -> typing.Union[DisciplineGQLModel, None]:
        result = await DisciplineGQLModel.load_with_loader(info=info, id=self.id)
        return result

@strawberry.mutation(description="Creates a new discipline", permission_classes=[OnlyForAuthentized])
async def discipline_insert(self, info: strawberry.types.Info, discipline: DisciplineInsertGQLModel) -> typing.Union[DisciplineGQLModel, InsertError[DisciplineGQLModel]]:
    result = await Insert[DisciplineGQLModel].DoItSafeWay(info=info, entity=discipline)
    return result

@strawberry.mutation(description="Updates an existing discipline", permission_classes=[OnlyForAuthentized])
async def discipline_update(self, info: strawberry.types.Info, discipline: DisciplineUpdateGQLModel) -> typing.Union[DisciplineGQLModel, UpdateError[DisciplineGQLModel]]:
    result = await Update[DisciplineGQLModel].DoItSafeWay(info=info, entity=discipline)
    return result

@strawberry.mutation(description="Deletes a discipline", permission_classes=[OnlyForAuthentized])
async def discipline_delete(self, info: strawberry.types.Info, discipline: DisciplineDeleteGQLModel) -> typing.Optional[DeleteError[DisciplineGQLModel]]:
    result = await Delete[DisciplineGQLModel].DoItSafeWay(info=info, entity=discipline)
    return result