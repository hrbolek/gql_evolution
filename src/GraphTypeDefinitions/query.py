import strawberry

from .ProjectGQLModel import ProjectQuery
from .FinanceGQLModel import FinanceQuery
from .MilestoneGQLModel import MilestoneQuery

@strawberry.type(description="""Type for query root""")
class Query(ProjectQuery, FinanceQuery, MilestoneQuery):
    pass
