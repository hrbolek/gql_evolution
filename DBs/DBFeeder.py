import datetime
import os
import json
import asyncio
import uuid
from functools import cache
from uoishelpers.feeders import ImportModels
from sqlalchemy.future import select
from DBs.DBDefinitions import (
    DisciplineModel,
    DisciplineSetModel,
    SummaryModel,
    ResultModel,
    NormModel
)

# Function to load demo data from a JSON file
def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if (key in ["startdate", "enddate", "lastchange", "created"]) or (key.endswith("_date")):
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                json_dict[key] = dateValueWOtzinfo

            if (key in ["id", "changedby", "createdby", "rbacobject"]) or ("_id" in key):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    print(key, value)

        return json_dict

    # Load data from 'systemdata.json' and parse datetime fields
    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

# Async function to initialize the database with demo data or predefined models
async def initDB(asyncSessionMaker):
    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            NormModel,
            ResultModel,
            SummaryModel,
            DisciplineSetModel,
            DisciplineModel
        ]
    else:
        dbModels = [
            NormModel,
            ResultModel,
            SummaryModel,
            DisciplineSetModel,
            DisciplineModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
