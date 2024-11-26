import strawberry
import uuid
import datetime as dt
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo

from .baseGQLModel import BaseGQLModel

DisciplineGQLModel = typing.Annotated["DisciplineGQLModel", strawberry.lazy(".DisciplineGQLModel")]
ResultGQLModel = typing.Annotated["ResultGQLModel", strawberry.lazy(".ResultGQLModel")]
SummaryGQLModel = typing.Annotated["SummaryGQLModel", strawberry.lazy(".SummaryGQLModel")]

@strawberry.type(description="Model representing a norm")

class NormGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "discipline_set_id": lambda row: row.discipline_set_id,
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
            "rbaobject_id": lambda row: row.rbaobject_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).NormModel
    
    id: uuid.UUID = strawberry.field()
    discipline_set_id: uuid.UUID = strawberry.field(description="ID of the discipline set")
    effective_date: dt.datetime = strawberry.field(description="Date when the norm is effective")
    expiration_date: dt.datetime = strawberry.field(description="Date when the norm expires")
    male: bool = strawberry.field(description="True if the norm is for male")
    female: bool = strawberry.field(description="True if the norm is for female")
    age_minimal: int = strawberry.field(description="Minimal age")
    age_maximal: int = strawberry.field(description="Maximal age")
    result_minimal_value: float = strawberry.field(description="Minimal value of the result")
    result_maximal_value: float = strawberry.field(description="Maximal value of the result")
    points: int = strawberry.field(description="Points")

    @strawberry.field(description="Returns a discipline for the norm")
    async def discipline(self, info: strawberry.types.Info) -> typing.Optional[DisciplineGQLModel]:
        from .DisciplineGQLModel import DisciplineGQLModel
        result = await DisciplineGQLModel.load_with_loader(info=info, id=self.discipline_set_id)
        return result
    
    @strawberry.field(description="Returns results for the norm")
    async def results(self, info: strawberry.types.Info) -> typing.List[ResultGQLModel]:
        from .ResultGQLModel import ResultGQLModel
        result = await ResultGQLModel.load_with_loader(info=info, id=self.discipline_set_id)
        return
    
    @strawberry.field(description="Returns a result template for the norm")
    async def template(self, info: strawberry.types.Info) -> typing.Optional[SummaryGQLModel]:
        from .SummaryGQLModel import SummaryGQLModel
        result = await SummaryGQLModel.load_with_loader(info=info, id=self.discipline_set_id)
        return result

@strawberry.field(description="Returns a norm by id")
async def norm_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[NormGQLModel]:
    result = await NormGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="Returns a list of norms")
async def norm_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> typing.List[NormGQLModel]:
    loader = getLoadersFromInfo(info).norms
    rows = await loader.page(skip, limit)
    return [NormGQLModel.from_sqlalchemy(row) for row in rows] if rows is not None else []