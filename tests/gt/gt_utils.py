import pytest
import logging
import uuid
import sqlalchemy
import datetime
import os.path
import json

def checkExpected(responseJSON, expectedJSON):
    def compareLists(left, right):
        if len(left) != len(right):
            return False
        for leftValue, rightValue in zip(left, right):
            if isinstance(leftValue, dict):
                if not compareDicts(leftValue, rightValue):
                    return False
            elif isinstance(leftValue, list):
                if not compareLists(leftValue, rightValue):
                    return False
            elif leftValue != right:
                return False
        return True
            
    def compareDicts(left, right):
        allKeys = set(left.keys()).update(right.keys())
        for key in allKeys:
            leftValue = left.get(key, None)
            rightValue = right.get(key, None)
            if (leftValue is not None) and (rightValue is None):
                return False
            if (leftValue is None) and (rightValue is not None):
                return False
            if isinstance(leftValue, dict):
                if not compareDicts(leftValue, rightValue):
                    return False
            elif isinstance(leftValue, list):
                if not compareLists(leftValue, rightValue):
                    return False
            elif leftValue != rightValue:
                return False
        return True
    responseDataValue = responseJSON.get("data", None)
    expectedDataValue = expectedJSON.get("data", None)
    responseErrorValue = responseJSON.get("error", None)
    expectedErrorValue = expectedJSON.get("error", None)

    if (responseDataValue is None) and (expectedDataValue is not None):
        return False
    if (responseDataValue is not None) and (expectedDataValue is None):
        return False
    if (responseErrorValue is not None) and (expectedErrorValue is None):
        return False
    if (responseErrorValue is None) and (expectedErrorValue is not None):
        return False
    
    if not compareDicts(responseDataValue, expectedDataValue):
        return False
    if not compareDicts(responseErrorValue, expectedErrorValue):
        return False
    return True


import os 
import re
dir_path = os.path.dirname(os.path.realpath(__file__))
print("dir_path", dir_path, flush=True)

location = "./src/tests/gqls"
location = re.sub(r"\\tests\\.+", r"\\tests\\gqls", dir_path)
# location
print("location", location, flush=True)
logging.info(f"Queries location {dir_path} => {location}")
def getQuery(tableName, queryName):
    queryFileName = f"{location}/{tableName}/{queryName}.gql"
    assert os.path.isfile(queryFileName), f"unable find query {queryName}@{tableName} {queryFileName}"
    logging.info(f"found query {queryName}@{tableName} {queryFileName}")
    with open(queryFileName, "r", encoding="utf-8") as f:
        query = f.read()
    return query

def getVariables(tableName, queryName):
    variableFileName = f"{location}/{tableName}/{queryName}.var.json"

    if os.path.isfile(variableFileName):
        with open(variableFileName, "r", encoding="utf-8") as f:
            variables = json.load(f)
    else:
        variables = {}
    return variables

def getExpectedResult(tableName, queryName):
    resultFileName = f"{location}/{tableName}/{queryName}.res.json"

    if os.path.isfile(resultFileName):
        with open(resultFileName, "r", encoding="utf-8") as f:
            expectedResult = json.load(f)
    else:
        expectedResult = None
    return expectedResult


def createByIdTest2(tableName, queryName=None, variables=None, expectedJson=None):
    @pytest.mark.asyncio
    async def result_test(SchemaExecutorDemo):
        queryRead = getQuery(tableName=tableName, queryName=("read" if queryName is None else queryName))
        _variables = variables
        if _variables is None:
            _variables = getVariables(tableName=tableName, queryName=("read" if queryName is None else queryName))
        if _variables == {}:
            queryReadPage = getQuery(tableName=tableName, queryName="readp")
            pageJson = await SchemaExecutorDemo(query=queryReadPage, variable_values={})

            logging.info(f"deriving variables from response to page query {pageJson}")
            pageData = pageJson.get("data", None)
            assert pageData is not None, f"during query {tableName}_by_id got page result with no data {pageJson}"
            [firstKey, *_] = pageData.keys()
            # firstKey = next(pageData.keys(), None)
            assert firstKey is not None, f"during query {tableName}_by_id got empty data {pageJson}"
            rows = pageData[firstKey]
            row = rows[0]
            assert "id" in row, f"during query {tableName}_by_id got page result but rows have no ids {row}"
            _variables = row
        
        _expectedJson = expectedJson
        if _expectedJson is None:
            _expectedJson = getExpectedResult(tableName=tableName, queryName="read")
        responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=_variables)
        if _expectedJson is not None:
            assert checkExpected(responseJson, _expectedJson), f"unexpected response \n{responseJson}\ninstead\n{_expectedJson}"
        else:
            assert "errors" not in responseJson, f"got errors {responseJson['errors']}"
            logging.info(f"query for {queryRead}@{tableName} with {_variables}, no tested response, got\n{responseJson}")
        
    return result_test

def createTest2(tableName, queryName, variables=None, expectedJson=None):
    @pytest.mark.asyncio
    async def result_test(SchemaExecutorDemo):
        query = getQuery(tableName=tableName, queryName=queryName)       
        _variables = variables
        if _variables is None:
            _variables = getVariables(tableName=tableName, queryName=queryName)       
        
        _expectedJson = expectedJson
        if _expectedJson is None:
            _expectedJson = getExpectedResult(tableName=tableName, queryName=queryName)
        responseJson = await SchemaExecutorDemo(query=query, variable_values=_variables)
        if _expectedJson is not None:
            assert checkExpected(responseJson, _expectedJson), f"unexpected response \n{responseJson}\ninstead\n{_expectedJson}"
        else:
            assert "errors" not in responseJson, f"query for {query} with {_variables}, got error {responseJson}"
            logging.debug(f"query for \n{query} with \n{_variables}, no tested response, got\n{responseJson}")
        
    return result_test

def createUpdateTest2(tableName, variables=None, expectedJson=None):
    queryName = "update"
    @pytest.mark.asyncio
    async def result_test(SchemaExecutorDemo):
        queryRead = getQuery(tableName=tableName, queryName="read")
        queryUpdate = getQuery(tableName=tableName, queryName=queryName)
        _variables = variables
        if _variables is None:
            _variables = getVariables(tableName=tableName, queryName=queryName)     
        if "id" not in _variables:
            queryReadPage = getQuery(tableName=tableName, queryName="readp")
            pageJson = await SchemaExecutorDemo(query=queryReadPage, variable_values={})
            logging.info(f"deriving variables from response to page query {pageJson}")
            pageData = pageJson.get("data", None)
            assert pageData is not None, f"during query {tableName}_by_id got page result with no data {pageJson}"
            [firstKey, *_] = pageData.keys()
            # firstKey = next(pageData.keys(), None)
            assert firstKey is not None, f"during query {tableName}_by_id got empty data {pageJson}"
            rows = pageData[firstKey]
            row = rows[0]
            assert "id" in row, f"during update query {tableName} got page result but rows have no ids {row}"

            _variables["id"] = row["id"]

        responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=_variables)
        responseData = responseJson.get("data")
        assert responseData is not None, f"got no data while asking for lastchange atribute {responseJson}"
        
        [responseEntity, *_] = responseData.values()
        assert responseEntity is not None, f"got no entity while asking for lastchange atribute {responseJson}"
        lastchange = responseEntity.get("lastchange", None)
        assert lastchange is not None, f"query read for table {tableName} is not asking for lastchange which is needed"
        _variables["lastchange"] = lastchange

        _expectedJson = expectedJson
        if _expectedJson is None:
            _expectedJson = getExpectedResult(tableName=tableName, queryName=queryName)
        responseJson = await SchemaExecutorDemo(query=queryUpdate, variable_values=_variables)
        if _expectedJson is not None:
            assert checkExpected(responseJson, expectedJson), f"unexpected response \n{responseJson}\ninstead\n{_expectedJson}"
        else:
            assert "errors" not in responseJson, f"update failed {responseJson}"
            logging.info(f"query for {queryUpdate} with {_variables}, no tested response")
        
    return result_test

def createDeleteTest2(tableName, variables=None, expectedJson=None):
    @pytest.mark.asyncio
    async def result_test(SchemaExecutorDemo):
        queryCreate = getQuery(tableName=tableName, queryName="create")
        queryDelete = getQuery(tableName=tableName, queryName="delete")
        _variables = variables
        if _variables is None:
            _variables = getVariables(tableName=tableName, queryName="delete")
        assert _variables != {}, f"variables must be set"

        responseJson = await SchemaExecutorDemo(query=queryCreate, variable_values=_variables)
        responseData = responseJson.get("data")
        assert responseData is not None, f"got no data while creating an entity for delete query {responseJson}"
        
        [responseEntity, *_] = responseData.values()
        assert responseEntity is not None, f"got no entity while asking for lastchange atribute {responseJson}"
        assert "lastchange" in responseEntity, f"query read for table {tableName} is not asking for lastchange which is needed see {responseJson}"
        assert "id" in responseEntity is not None, f"variables must have an 'id'"
        
        _variables = responseEntity
        _expectedJson = expectedJson
        if _expectedJson is None:
            _expectedJson = getExpectedResult(tableName=tableName, queryName="delete")
        responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=_variables)
        if _expectedJson is not None:
            assert checkExpected(responseJson, expectedJson), f"unexpected response \n{responseJson}\ninstead\n{_expectedJson}"
        else:
            assert "errors" not in responseJson, f"update failed {responseJson}"
            logging.info(f"query for {queryDelete} with {_variables}, no tested response")
        
    return result_test