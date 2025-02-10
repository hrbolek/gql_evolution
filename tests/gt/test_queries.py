import pytest
import asyncio
import logging
import uuid
import sqlalchemy
import json
import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from GQLs.BaseGQLModel import BaseGQLModel
from DBs.DBDefinitions import DisciplineModel, DisciplineSetModel, SummaryModel, ResultModel, NormModel


myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

@pytest.mark.asyncio
async def test_result_test(NoRole_UG_Server):
    response = await NoRole_UG_Server(query=myquery, variables={})
    print("response", response, flush=True)
    logging.info(f"response {response}")
    pass

from .gt_utils import (
    getQuery,
    createByIdTest2,
    createUpdateTest2,
    createTest2,
    createDeleteTest2
)

from GQLs.GraphResolvers import (
    resolveDisciplineById,
    resolveDisciplineAll,
    resolveInsertDiscipline,
    resolveUpdateDiscipline,
    resolveDisciplineSetById,
    resolveDisciplineSetAll,
    resolveInsertDisciplineSet,
    resolveUpdateDisciplineSet,
    resolveSummaryById,
    resolveSummaryAll,
    resolveInsertSummary,
    resolveUpdateSummary,
    resolveResultById,
    resolveResultAll,
    resolveInsertResult,
    resolveUpdateResult,
    resolveNormById,
    resolveNormAll,
    resolveInsertNorm,
    resolveUpdateNorm,
)

from GQLs.GraphPermissions import (
    BasePermission,
    GroupEditorPermission,
    UserEditorPermission,
    UserGDPRPermission,
    AsyncSessionFromInfo,
    UserFromInfo
)

test_discipline_by_id = createByIdTest2(tableName="disciplines")
#test_discipline_coverage = createByIdTest2(tableName="disciplines", queryName="coverage")
test_discipline_update = createUpdateTest2(tableName="disciplines", variables={"name": "newname"})
test_discipline_create = createTest2(tableName="disciplines", queryName="create", variables={"name": "newname"})
test_discipline_delete = createDeleteTest2(tableName="disciplines", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "newname"})

test_disciplineSet_by_id = createByIdTest2(tableName="discipline_sets")
#test_disciplineSet_coverage = createByIdTest2(tableName="discipline_sets", queryName="coverage")
test_disciplineSet_update = createUpdateTest2(tableName="discipline_sets", variables={"name": "newname"})
test_disciplineSet_create = createTest2(tableName="discipline_sets", queryName="create", variables={"name": "newname"})
test_disciplineSet_delete = createDeleteTest2(tableName="discipline_sets", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463534", "name": "newname"})

test_norm_by_id = createByIdTest2(tableName="norms")
#test_norm_coverage = createByIdTest2(tableName="norms", queryName="coverage")
test_norm_update = createUpdateTest2(tableName="norms", variables={"effective_date": "2025-02-05T00:00:00"})
test_norm_create = createTest2(tableName="norms", queryName="create", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463535"})
test_norm_delete = createDeleteTest2(tableName="norms", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463535"})

test_result_by_id = createByIdTest2(tableName="results")
#test_result_coverage = createByIdTest2(tableName="results", queryName="coverage")
test_result_update = createUpdateTest2(tableName="results", variables={"evaluation_date": "2025-02-05T00:00:01"})
test_result_create = createTest2(tableName="results", queryName="create", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463536"})
test_result_delete = createDeleteTest2(tableName="results", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463536"})

test_summary_by_id = createByIdTest2(tableName="summaries")
#test_summary_coverage = createByIdTest2(tableName="summaries", queryName="coverage")
test_summary_update = createUpdateTest2(tableName="summaries", variables={"effective_date": "2025-02-05T00:00:02"})
test_summary_create = createTest2(tableName="summaries", queryName="create", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463537"})
test_summary_delete = createDeleteTest2(tableName="summaries", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463537"})

def test_get_table_resolvers_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseGQLModel.get_table_resolvers()