import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .ProjectGQLModel import ProjectQuery
from .FinanceGQLModel import FinanceQuery
from .MilestoneGQLModel import MilestoneQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, ProjectQuery, FinanceQuery, MilestoneQuery):
    pass
