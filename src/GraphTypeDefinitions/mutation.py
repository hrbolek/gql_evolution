import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .ProjectGQLModel import ProjectMutation
from .FinanceGQLModel import FinanceMutation
from .MilestoneGQLModel import MilestoneMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, ProjectMutation, FinanceMutation, MilestoneMutation):
    pass

