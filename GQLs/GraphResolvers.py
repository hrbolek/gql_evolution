from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb
from DBs.DBDefinitions import (
    DisciplineModel,
    DisciplineSetModel,
    SummaryModel,
    ResultModel,
    NormModel,
)

# 🔹 Discipline resolvers
resolveDisciplineById = createEntityByIdGetter(DisciplineModel)
resolveDisciplineAll = createEntityGetter(DisciplineModel)
resolveInsertDiscipline = createInsertResolver(DisciplineModel)
resolveUpdateDiscipline = createUpdateResolver(DisciplineModel)

# 🔹 DisciplineSet resolvers
resolveDisciplineSetById = createEntityByIdGetter(DisciplineSetModel)
resolveDisciplineSetAll = createEntityGetter(DisciplineSetModel)
resolveInsertDisciplineSet = createInsertResolver(DisciplineSetModel)
resolveUpdateDisciplineSet = createUpdateResolver(DisciplineSetModel)

# 🔹 Summary resolvers
resolveSummaryById = createEntityByIdGetter(SummaryModel)
resolveSummaryAll = createEntityGetter(SummaryModel)
resolveInsertSummary = createInsertResolver(SummaryModel)
resolveUpdateSummary = createUpdateResolver(SummaryModel)

# 🔹 Result resolvers
resolveResultById = createEntityByIdGetter(ResultModel)
resolveResultAll = createEntityGetter(ResultModel)
resolveInsertResult = createInsertResolver(ResultModel)
resolveUpdateResult = createUpdateResolver(ResultModel)

# 🔹 Norm resolvers
resolveNormById = createEntityByIdGetter(NormModel)
resolveNormAll = createEntityGetter(NormModel)
resolveInsertNorm = createInsertResolver(NormModel)
resolveUpdateNorm = createUpdateResolver(NormModel)

# 🔹 Vztahy (1:N)
resolveDisciplinesForUser = create1NGetter(DisciplineModel, foreignKeyName="user_id")
resolveDisciplineSetsForUser = create1NGetter(DisciplineSetModel, foreignKeyName="user_id")
resolveResultsForUser = create1NGetter(ResultModel, foreignKeyName="user_id")
resolveNormsForUser = create1NGetter(NormModel, foreignKeyName="user_id")