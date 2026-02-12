import os

from functools import cache
from uoishelpers.feeders import ImportModels
from uoishelpers.dataloaders import readJsonFile

from src.DBDefinitions import (
    ProjectModel,
    FinanceModel,
    MilestoneModel,
)

get_demodata = lambda :readJsonFile(jsonFileName="./systemdata.json")
async def initDB(asyncSessionMaker, filename="./systemdata.json"):

    dbModels = [
    ]

    isDemo = os.environ.get("DEMODATA", None) in ["True", "true", True]
    if isDemo:
        print("Demo mode", flush=True)
        dbModels = [
            ProjectModel,
            FinanceModel,
            MilestoneModel,
        ]
        

    jsonData = readJsonFile(filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    
    print("Data initialized", flush=True)

async def backupDB(asyncSessionMaker, filename="./systemdata.backup.json"):
    import sqlalchemy
    import dataclasses
    import json
    from src.DBDefinitions.BaseModel import IDType

    dbModels = [
        ProjectModel,
        FinanceModel,
        MilestoneModel,
    ]
    data = []
    async with asyncSessionMaker() as session:
        for model in dbModels:
            sqlquery = sqlalchemy.select(model)
            rows = await session.execute(sqlquery)
            # vsechny radky do dict
            rowsdict = {}
            for row in rows:
                # print(row)
                asdict = dataclasses.asdict(row[0])
                id = asdict.get("id", None)
                if id is None: continue
                rowsdict[id] = asdict
            # vsechny primarní klice do ids
            ids = set(rowsdict.keys())
            todo = set()
            done = set()
            chunk_id = 0
            while len(done) < len(ids):
                for row in rowsdict.values():
                    id = row.get("id", None)
                    if id in done: continue
                    skip_this_id = False
                    for key, value in row.items():
                        if key == "id": continue
                        # if not isinstance(value, IDType): continue
                        if value is None: continue
                        if value not in ids: continue
                        if value not in done: 
                            # print(row, key, value)
                            skip_this_id = True
                            break
                            # primarni klic je zpracovatelny, nemame zavislost na nezpracovanych klicich
                    if skip_this_id: continue
                    row["_chunk"] = chunk_id
                    todo.add(id)
                print(f"{model.__tablename__} chunk {chunk_id} todo/done/all {len(todo)}/{len(done)}/{len(ids)}")
                if len(todo) == 0: break
                done = done.union(todo)
                todo = set()
                chunk_id += 1
            data.append({
                model.__tablename__: list(rowsdict.values())
            })
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=str)
    
    print("backup done", flush=True)