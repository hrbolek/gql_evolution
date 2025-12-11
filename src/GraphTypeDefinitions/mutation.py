import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .ProjectGQLModel import ProjectMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, ProjectMutation):
    pass

