import strawberry
import typing
ResultGQLModel = typing.Annotated["ResultGQLModel", strawberry.lazy(".ResultGQLModel")]
@strawberry.type(description="Type for query root")
class UserGQLModel:
    id: strawberry.ID


    @strawberry.field(description="Returns hello world")
    async def results(
        self,
        info: strawberry.types.Info,
    ) -> typing.List[ResultGQLModel]:
        pass