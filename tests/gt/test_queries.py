import pytest
import logging
import uuid
import sqlalchemy
import json
import datetime

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

test_discipline_by_id = createByIdTest2(tableName="disciplines")
test_discipline_coverage = createByIdTest2(tableName="disciplines", queryName="coverage")
test_discipline_update = createUpdateTest2(tableName="disciplines", variables={"name": "newname"})
test_discipline_create = createTest2(tableName="disciplines", queryName="create", variables={"name": "newname"})
test_discipline_delete = createDeleteTest2(tableName="disciplines", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "newname"})

test_discipline = createByIdTest2(tableName="tv_dicsiplines", variables={"id": "7dcf3d10-3a41-4c36-9700-99d885a1e474"})
test_discipline_create = createTest2(
    tableName="tv_dicsiplines", 
    queryName="create",
    variables={
        "id": "bab05e55-3f92-40b5-9272-4b66a368138",
        "summary_id": "7dcf3d10-3a41-4c36-9700-99d885a1e474",
        }
    )

@pytest.mark.asyncio
async def test_discipline_update(SchemaExecutorDemo):
    tableName = "tv_disciplines"
    variables = {
        "id": "e622232d-e34d-4efc-8094-74ace62c7989",
    }
    queryRead = getQuery(tableName=tableName, queryName="read")
    queryUpdate = getQuery(tableName=tableName, queryName="update")
    _variables = variables

    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=_variables)
    responseData = responseJson.get("data")
    assert responseData is not None, f"got no data while asking for lastchange attribute {responseJson}"
    
    [responseEntity, *_] = responseData.values()
    assert responseEntity is not None, f"got no entity while asking for lastchange attribute {responseJson}"
    lastchange = responseEntity.get("lastchange", None)
    assert lastchange is not None, f"query read for table {tableName} is not asking for lastchange which is needed"
    _variables["lastchange"] = lastchange

    responseJson = await SchemaExecutorDemo(query=queryUpdate, variable_values=_variables)
    assert "errors" not in responseJson, f"update failed {responseJson}"
    logging.info(f"query for {queryUpdate} with {_variables}, no tested response")

    pass

@pytest.mark.asyncio
async def test_discipline_delete(SchemaExecutorDemo):
    tableName = "tv_disciplines"
    variables = {
        "id": "e622232d-e34d-4efc-8094-74ace62c7989",
    }
    queryRead = getQuery(tableName=tableName, queryName="read")
    queryDelete = getQuery(tableName=tableName, queryName="delete")
    _variables = variables

    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=_variables)
    responseData = responseJson.get("data")
    assert responseData is not None, f"got no data while asking for lastchange attribute {responseJson}"
    
    [responseEntity, *_] = responseData.values()
    assert responseEntity is not None, f"got no entity while asking for lastchange attribute {responseJson}"
    lastchange = responseEntity.get("lastchange", None)
    assert lastchange is not None, f"query read for table {tableName} is not asking for lastchange which is needed"
    _variables["lastchange"] = lastchange

    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=_variables)
    assert "errors" not in responseJson, f"delete failed {responseJson}"
    logging.info(f"query for {queryDelete} with {_variables}, no tested response")

    pass
