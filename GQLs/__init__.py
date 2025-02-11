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
    
from .ResultGQLModel import result_insert, result_update, result_delete
from .DisciplineGQLModel import discipline_insert, discipline_update, discipline_delete
from .DisciplineSetGQLModel import discipline_set_insert, discipline_set_update, discipline_set_delete
from .SummaryGQLModel import summary_insert, summary_update, summary_delete
from .NormGQLModel import norm_insert, norm_update, norm_delete

# Define the root mutation type with a description
@strawberry.type(description="Type for mutation root")
class Mutation:
    
    # Include other mutations
    result_insert = result_insert
    result_update = result_update
    result_delete = result_delete
    discipline_insert = discipline_insert
    discipline_update = discipline_update
    discipline_delete = discipline_delete
    discipline_set_insert = discipline_set_insert
    discipline_set_update = discipline_set_update
    discipline_set_delete = discipline_set_delete
    summary_insert = summary_insert
    summary_update = summary_update
    summary_delete = summary_delete
    norm_insert = norm_insert
    norm_update = norm_update
    norm_delete = norm_delete

from uoishelpers.schema import WhoAmIExtension

# Create the GraphQL schema with the defined query and mutation types
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types = [DisciplineGQLModel, DisciplineSetGQLModel, ResultGQLModel, SummaryGQLModel, NormGQLModel],
    extensions = [WhoAmIExtension]
)
