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

@strawberry.type(description="Model representing a norm")
class NormGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "effective_date": lambda row: row.effective_date,
            "expiration_date": lambda row: row.expiration_date,
            "male": lambda row: row.male,
            "female": lambda row: row.female,
            "age_minimal": lambda row: row.age_minimal,
            "age_maximal": lambda row: row.age_maximal,
            "result_minimal_value": lambda row: row.result_minimal_value,
            "result_maximal_value": lambda row: row.result_maximal_value,
            "points": lambda row: row.points,
            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbacobject_id": lambda row: row.rbacobject_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).NormModel
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).NormModel
    
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm is effective", default = None, permission_classes=[OnlyForAuthentized])
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm expires", default = None, permission_classes=[OnlyForAuthentized])
    male: typing.Optional[bool] = strawberry.field(description="True if the norm is for male", default = None, permission_classes=[OnlyForAuthentized])
    female: typing.Optional[bool] = strawberry.field(description="True if the norm is for female", default = None, permission_classes=[OnlyForAuthentized])
    age_minimal: typing.Optional[int] = strawberry.field(description="Minimal age", default = None, permission_classes=[OnlyForAuthentized])
    age_maximal: typing.Optional[int] = strawberry.field(description="Maximal age", default = None, permission_classes=[OnlyForAuthentized])
    result_minimal_value: typing.Optional[float] = strawberry.field(description="Minimal value of the result", default = None, permission_classes=[OnlyForAuthentized])
    result_maximal_value: typing.Optional[float] = strawberry.field(description="Maximal value of the result", default = None, permission_classes=[OnlyForAuthentized])
    points: typing.Optional[int] = strawberry.field(description="Points", default = None, permission_classes=[OnlyForAuthentized])
    
    @strawberry.field(description="Returns a summaries for the norm", permission_classes=[OnlyForAuthentized])
    async def summaries(self, info: strawberry.types.Info) -> typing.List[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=self.summary_id)
        return result
    
@createInputs
@dataclasses.dataclass
class NormInputFilter:
    effective_date: dt.datetime
    expiration_date: dt.datetime
    male: bool
    female: bool
    age_minimal: int
    age_maximal: int
    result_minimal_value: float
    result_maximal_value: float
    points: int

# Queries

@strawberry.field(description="Returns a norm by id", permission_classes=[OnlyForAuthentized])
async def norm_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[NormGQLModel]:
    result = await NormGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of norms", permission_classes=[OnlyForAuthentized])
async def norm_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[NormGQLModel]:
    loader = NormGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [NormGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []

norm_page = strawberry.field(
        description="""Finds paged norms""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[NormGQLModel](whereType=NormInputFilter)
        ) 

# Mutations

@strawberry.input(description="Definition of a norm used for insert")
class NormInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the norm", default=None)
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm is effective", default=None)
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm expires", default=None)
    male: typing.Optional[bool] = strawberry.field(description="True if the norm is for male", default=None)
    female: typing.Optional[bool] = strawberry.field(description="True if the norm is for female", default=None)
    age_minimal: typing.Optional[int] = strawberry.field(description="Minimal age", default=None)
    age_maximal: typing.Optional[int] = strawberry.field(description="Maximal age", default=None)
    result_minimal_value: typing.Optional[float] = strawberry.field(description="Minimal value of the result", default=None)
    result_maximal_value: typing.Optional[float] = strawberry.field(description="Maximal value of the result", default=None)
    points: typing.Optional[int] = strawberry.field(description="Points", default=None)
    createdby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the user who created this record", default=None)

@strawberry.input(description="Definition of a norm used for update")
class NormUpdateGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the norm")
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm is effective", default=None)
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm expires", default=None)
    male: typing.Optional[bool] = strawberry.field(description="True if the norm is for male", default=None)
    female: typing.Optional[bool] = strawberry.field(description="True if the norm is for female", default=None)
    age_minimal: typing.Optional[int] = strawberry.field(description="Minimal age", default=None)
    age_maximal: typing.Optional[int] = strawberry.field(description="Maximal age", default=None)
    result_minimal_value: typing.Optional[float] = strawberry.field(description="Minimal value of the result", default=None)
    result_maximal_value: typing.Optional[float] = strawberry.field(description="Maximal value of the result", default=None)
    points: typing.Optional[int] = strawberry.field(description="Points", default=None)
    changedby_id: typing.Optional[uuid.UUID] = strawberry.field(description="ID of the user who last modified this record", default=None)

@strawberry.input(description="Definition of a norm used for delete")
class NormDeleteGQLModel:
    lastchange: dt.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="ID of the norm")

#####

@strawberry.type(description="Result of a mutation for a norm")
class NormMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="ID of the norm", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK / FAIL)", default=None)

    @strawberry.field(description="Returns the norm")
    async def norm(self, info: strawberry.types.Info) -> typing.Union[NormGQLModel, None]:
        result = await NormGQLModel.load_with_loader(info=info, id=self.id)
        return result

@strawberry.mutation(description="Creates a new norm", permission_classes=[OnlyForAuthentized])
async def norm_insert(self, info: strawberry.types.Info, norm: NormInsertGQLModel) -> typing.Union[NormGQLModel, InsertError[NormGQLModel]]:
    result = await Insert[NormGQLModel].DoItSafeWay(info=info, entity=norm)
    return result

@strawberry.mutation(description="Updates an existing norm", permission_classes=[OnlyForAuthentized])
async def norm_update(self, info: strawberry.types.Info, norm: NormUpdateGQLModel) -> typing.Union[NormGQLModel, UpdateError[NormGQLModel]]:
    result = await Update[NormGQLModel].DoItSafeWay(info=info, entity=norm)
    return result

@strawberry.mutation(description="Deletes a norm", permission_classes=[OnlyForAuthentized])
async def norm_delete(self, info: strawberry.types.Info, norm: NormDeleteGQLModel) -> typing.Optional[DeleteError[NormGQLModel]]:
    result = await Delete[NormGQLModel].DoItSafeWay(info=info, entity=norm)
    return result