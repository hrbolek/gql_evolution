import strawberry

# Define the root query type with a description
@strawberry.type(description="Type for query root")
class Query:
    @strawberry.field(
        description="Returns hello world"
    )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"

# Define the root mutation type with a description
@strawberry.type(description="Type for mutation root")
class Mutation:
    @strawberry.field(
        description="Returns hello world"
    )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"

# Create the GraphQL schema with the defined query and mutation types
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)