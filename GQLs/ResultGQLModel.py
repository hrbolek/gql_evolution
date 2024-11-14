from typing import List, Union
import typing
import strawberry as strawberryA


UserGQLModel = typing.Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
# Define the ResultGQLModel GraphQL type for results, with federation support
@strawberryA.federation.type(extend=True, keys=["id"])
class ResultGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)
    _value: float

    @strawberryA.field(description="Value of the result")
    def value(self) -> float:
        return self._value
    
    @strawberryA.field(description="User who has the result")
    async def student(self) -> typing.Optional["UserGQLModel"]:
        pass
    @strawberryA.field(description="User who has the result")
    async def examiner(self) -> typing.Optional["UserGQLModel"]:
        pass

# Resolver function to fetch results from the database with pagination
# @strawberryA.field(description="Returns a single result by ID")
# async def resolveResultAll(session: AsyncSession, skip: int, limit: int) -> List[ResultGQLModel]:
#     result_stmt = select(ResultGQLModel).offset(skip).limit(limit)
#     result = await session.execute(result_stmt)
#     results = result.scalars().all()
    
#     return [ResultGQLModel(id=r.id, _value=r.value) for r in results]

# Define the root query type with a description
    
@strawberryA.field(description="Returns a single result by ID")
async def result_by_id(self, info: strawberryA.types.Info, id: strawberryA.ID) -> Union[ResultGQLModel, None]:
    pass
