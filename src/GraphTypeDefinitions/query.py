import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .ProjectGQLModel import ProjectQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, ProjectQuery):
    pass
