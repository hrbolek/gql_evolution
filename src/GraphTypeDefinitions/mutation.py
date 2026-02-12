import strawberry

from .ProjectGQLModel import ProjectMutation
from .FinanceGQLModel import FinanceMutation
from .MilestoneGQLModel import MilestoneMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(ProjectMutation, FinanceMutation, MilestoneMutation):
    pass

