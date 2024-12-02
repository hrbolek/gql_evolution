import strawberry

# Import the required models
from .DisciplineGQLModel import DisciplineGQLModel
from .DisciplineSetGQLModel import DisciplineSetGQLModel
from .ResultGQLModel import ResultGQLModel
from .SummaryGQLModel import SummaryGQLModel
from .NormGQLModel import NormGQLModel

from .ResultGQLModel import result_by_id, result_page
from .DisciplineGQLModel import discipline_by_id, discipline_page
from .DisciplineSetGQLModel import discipline_set_by_id, discipline_set_page
from .SummaryGQLModel import summary_by_id, summary_page
from .NormGQLModel import norm_by_id, norm_page

# Define the root query type with a description
@strawberry.type(description="Type for query root")
class Query:
    @strawberry.field(description="Returns hello world")
    async def hello(self, info: strawberry.types.Info) -> str:
        return "hello world"
    
    # Include other queries
    result_by_id = result_by_id
    result_page = result_page
    discipline_by_id = discipline_by_id
    discipline_page = discipline_page
    discipline_set_by_id = discipline_set_by_id
    discipline_set_page = discipline_set_page
    summary_by_id = summary_by_id
    summary_page = summary_page
    norm_by_id = norm_by_id
    norm_page = norm_page

# Define the root mutation type with a description
@strawberry.type(description="Type for mutation root")
class Mutation:
    @strawberry.field(description="Returns hello world")
    async def hello(self, info: strawberry.types.Info) -> str:
        return "hello world"
    
    # Include other mutations

from uoishelpers.schema import WhoAmIExtension

# Create the GraphQL schema with the defined query and mutation types
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types = [DisciplineGQLModel, DisciplineSetGQLModel, ResultGQLModel, SummaryGQLModel, NormGQLModel],
    extensions = [WhoAmIExtension]
)
