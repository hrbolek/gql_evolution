import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

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
    
    effective_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm is effective", default = None)
    expiration_date: typing.Optional[dt.datetime] = strawberry.field(description="Date when the norm expires", default = None)
    male: typing.Optional[bool] = strawberry.field(description="True if the norm is for male", default = None)
    female: typing.Optional[bool] = strawberry.field(description="True if the norm is for female", default = None)
    age_minimal: typing.Optional[int] = strawberry.field(description="Minimal age", default = None)
    age_maximal: typing.Optional[int] = strawberry.field(description="Maximal age", default = None)
    result_minimal_value: typing.Optional[float] = strawberry.field(description="Minimal value of the result", default = None)
    result_maximal_value: typing.Optional[float] = strawberry.field(description="Maximal value of the result", default = None)
    points: typing.Optional[int] = strawberry.field(description="Points", default = None)
    
    @strawberry.field(description="Returns a summaries for the norm")
    async def summaries(self, info: strawberry.types.Info) -> typing.List[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=self.discipline_id)
        return result

@strawberry.field(description="Returns a norm by id")
async def norm_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[NormGQLModel]:
    result = await NormGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of norms")
async def norm_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[NormGQLModel]:
    loader = NormGQLModel.getloader(info)
    rows = await loader.page(skip, limit)
    return [NormGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []