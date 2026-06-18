"""GraphQL contract tests for EventGQLModel.

One file is intentionally dedicated to one GQL model.  The tests use the public
GraphQL API defined for EventGQLModel in
``src/GraphTypeDefinitions/Domain_Events/EventGQLModel.py``:

* queries: ``eventPage`` and ``eventById``
* mutations: ``eventInsert``, ``eventUpdate``, ``eventEnsureInvitations`` and
  ``eventDelete``

The tests are explicit integration tests.  They execute GraphQL operations
against the test schema instead of calling resolvers or services directly.
"""

from __future__ import annotations

import uuid

import pytest
import logging
from tests.support.asserts import assert_insert, assert_update, assert_delete, assert_same, assert_typename_with_error

async def event_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def event_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("eventDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

@pytest.mark.asyncio
async def test_event_(SchemaExecutor, CreateMutation):
    """Test eventInsert, eventUpdate and eventDelete mutations."""
    query = CreateMutation("eventInsert")

    logging.info(f"Executing query: \n{query}")
    # assert False

    event_id = str(uuid.uuid4())
    inserted = None
    updated = None

    try:
        # Insert a new event
        insert_variables = {
            "id": event_id,
            "name": "pytest EventGQLModel mutation",
            "nameEn": "pytest EventGQLModel mutation EN",
            "description": "description for pytest EventGQLModel mutation",
            "mastereventId": "a64871f8-2308-48ff-adb2-33fb0b0741f1",
            "startdate": "2026-01-01T10:00:00",
            "enddate": "2026-01-02T10:00:00",
            "place": "pytest graphql",
        }
        insert_result = await event_insert(SchemaExecutor, CreateMutation, insert_variables)
        inserted = assert_insert(insert_result)
        assert inserted["id"] == event_id

        # Update the event
        update_variables = {
                "id": event_id,
                "lastchange": inserted["lastchange"],
                "name": "pytest EventGQLModel mutation updated",
                "nameEn": "pytest EventGQLModel mutation updated EN",
                "description": "updated by EventGQLModel mutation test",
                "startdate": "2026-01-03T12:00:00",
                "enddate": "2026-01-03T14:30:00",
                "place": "pytest graphql updated",
        }
        update_result = await event_update(SchemaExecutor, CreateMutation, update_variables)
        updated = assert_update(update_result)
        assert updated["id"] == event_id

    finally:
        # Clean up by deleting the event
        if updated is not None:
            delete_variables = {
                "id": event_id, "lastchange": updated.get("lastchange")
            }
            delete_result = await event_delete(SchemaExecutor, CreateMutation, delete_variables)
            assert_delete(delete_result)
        elif inserted is not None:
            delete_variables = {"id": event_id, "lastchange": inserted.get("lastchange")}
            delete_result = await event_delete(SchemaExecutor, CreateMutation, delete_variables)
            assert_delete(delete_result)



# EVENT_FIELDS = """
#   __typename
#   id
#   created
#   lastchange
#   createdbyId
#   changedbyId
#   rbacobjectId
#   name
#   nameEn
#   description
#   startdate
#   enddate
#   place
#   valid
#   mastereventId
#   duration
#   durationSeconds: duration(unit: SECONDS)
#   durationMinutes: duration(unit: MINUTES)
#   durationHours: duration(unit: HOURS)
#   durationDays: duration(unit: DAYS)
#   durationWeeks: duration(unit: WEEKS)
#   subevents {
#     __typename
#     id
#     name
#     mastereventId
#   }
#   userInvitations {
#     __typename
#     id
#     eventId
#     userId
#     stateId
#   }
# """

# EVENT_ERROR_FIELDS = """
#   __typename
#   ... on EventGQLModelInsertError {
#     msg
#     code
#     location
#   }
#   ... on EventGQLModelUpdateError {
#     msg
#     code
#     location
#     Entity {
#       __typename
#       id
#       name
#     }
#   }
#   ... on EventGQLModelDeleteError {
#     msg
#     code
#     location
#     Entity {
#       __typename
#       id
#       name
#     }
#   }
# """

# ORGANIZER_STATE_ID = "3265a488-bbfa-4c59-946c-7a7b059ee4f0"
# INVITED_STATE_ID = "01b96c1d-8389-4267-a859-d8116e1c32f3"


# async def _event_insert(SchemaExecutor, *, event_id: str, name: str, masterevent_id: str | None = None):
#     result = await SchemaExecutor(
#         query=f"""
#         mutation EventInsert($event: EventInsertGQLModel!) {{
#           eventInsert(event: $event) {{
#             ... on EventGQLModel {{
# {EVENT_FIELDS}
#             }}
# {EVENT_ERROR_FIELDS}
#           }}
#         }}
#         """,
#         variable_values={
#             "event": {
#                 "id": event_id,
#                 "name": name,
#                 "nameEn": f"{name} EN",
#                 "description": f"description for {name}",
#                 "startdate": "2026-01-01T10:00:00",
#                 "enddate": "2026-01-02T10:00:00",
#                 "place": "pytest graphql",
#                 "mastereventId": masterevent_id,
#             }
#         },
#     )
#     return assert_insert(result)


# async def _event_delete(SchemaExecutor, *, event_id: str, lastchange: str | None):
#     if lastchange is None:
#         return None
#     result = await SchemaExecutor(
#         query=f"""
#         mutation EventDelete($event: EventDeleteGQLModel!) {{
#           eventDelete(event: $event) {{
# {EVENT_ERROR_FIELDS}
#           }}
#         }}
#         """,
#         variable_values={"event": {"id": event_id, "lastchange": lastchange}},
#     )
#     return assert_delete(result)


# @pytest.mark.explicit
# @pytest.mark.asyncio
# async def test_EventGQLModel_queries_return_all_model_attributes(SchemaExecutor):
#     """eventPage and eventById expose EventGQLModel scalar and vector fields."""

#     event_id = str(uuid.uuid4())
#     child_id = str(uuid.uuid4())
#     invitation_user_id = str(uuid.uuid4())
#     root = None
#     child = None

#     try:
#         root = await _event_insert(SchemaExecutor, event_id=event_id, name="pytest EventGQLModel query root")
#         child = await _event_insert(
#             SchemaExecutor,
#             event_id=child_id,
#             name="pytest EventGQLModel query child",
#             masterevent_id=event_id,
#         )

#         ensure_result = await SchemaExecutor(
#             query=f"""
#             mutation EventEnsureInvitations($event: EventEnsureUserInvitationsModel!) {{
#               eventEnsureInvitations(event: $event) {{
#                 ... on EventGQLModel {{
# {EVENT_FIELDS}
#                 }}
# {EVENT_ERROR_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={
#                 "event": {
#                     "id": event_id,
#                     "userInvitations": [
#                         {
#                             "userId": invitation_user_id,
#                             "stateId": INVITED_STATE_ID,
#                         }
#                     ],
#                 }
#             },
#         )
#         ensured = assert_update(ensure_result)
#         assert ensured["id"] == event_id

#         page_result = await SchemaExecutor(
#             query=f"""
#             query EventPage($where: EventInputFilter, $limit: Int!) {{
#               eventPage(where: $where, limit: $limit) {{
# {EVENT_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={"where": {"id": {"_eq": event_id}}, "limit": 1},
#         )
#         assert page_result.get("errors") is None
#         page = page_result.get("data", {}).get("eventPage")
#         assert isinstance(page, list)
#         assert len(page) == 1
#         event_from_page = page[0]
#         assert event_from_page["id"] == event_id
#         assert event_from_page["name"] == root["name"]
#         assert event_from_page["nameEn"] == root["nameEn"]
#         assert event_from_page["description"] == root["description"]
#         assert event_from_page["startdate"] == root["startdate"]
#         assert event_from_page["enddate"] == root["enddate"]
#         assert event_from_page["place"] == root["place"]
#         assert event_from_page["mastereventId"] is None
#         assert event_from_page["duration"] == 24 * 60
#         assert event_from_page["durationSeconds"] == 24 * 60 * 60
#         assert event_from_page["durationMinutes"] == 24 * 60
#         assert event_from_page["durationHours"] == 24
#         assert event_from_page["durationDays"] == 1
#         assert event_from_page["durationWeeks"] == pytest.approx(1 / 7)
#         assert isinstance(event_from_page["valid"], bool)
#         assert isinstance(event_from_page["subevents"], list)
#         assert any(row["id"] == child_id and row["mastereventId"] == event_id for row in event_from_page["subevents"])
#         assert isinstance(event_from_page["userInvitations"], list)
#         assert any(row["userId"] == invitation_user_id and row["stateId"] == INVITED_STATE_ID for row in event_from_page["userInvitations"])

#         by_id_result = await SchemaExecutor(
#             query=f"""
#             query EventById($id: UUID!) {{
#               eventById(id: $id) {{
# {EVENT_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={"id": event_id},
#         )
#         event_by_id = assert_read(by_id_result)
#         assert event_by_id["id"] == event_id
#         assert event_by_id["name"] == root["name"]
#         assert event_by_id["nameEn"] == root["nameEn"]
#         assert event_by_id["description"] == root["description"]
#         assert event_by_id["startdate"] == root["startdate"]
#         assert event_by_id["enddate"] == root["enddate"]
#         assert event_by_id["place"] == root["place"]
#         assert event_by_id["durationHours"] == 24
#         assert any(row["id"] == child_id for row in event_by_id["subevents"])
#         assert any(row["userId"] == invitation_user_id for row in event_by_id["userInvitations"])

#     finally:
#         if child is not None:
#             await _event_delete(SchemaExecutor, event_id=child_id, lastchange=child.get("lastchange"))
#         if root is not None:
#             # Refresh the root timestamp after eventEnsureInvitations may have
#             # touched related data.  If refresh fails, fall back to the inserted
#             # row timestamp and let assert_delete show the real API error.
#             refresh = await SchemaExecutor(
#                 query="""
#                 query EventById($id: UUID!) {
#                   eventById(id: $id) {
#                     __typename
#                     id
#                     lastchange
#                   }
#                 }
#                 """,
#                 variable_values={"id": event_id},
#             )
#             lastchange = root.get("lastchange")
#             if refresh.get("errors") is None and refresh.get("data", {}).get("eventById"):
#                 lastchange = refresh["data"]["eventById"].get("lastchange")
#             await _event_delete(SchemaExecutor, event_id=event_id, lastchange=lastchange)


# @pytest.mark.explicit
# @pytest.mark.asyncio
# async def test_EventGQLModel_mutations_cover_defined_event_operations(SchemaExecutor):
#     """eventInsert, eventUpdate, eventEnsureInvitations and eventDelete work through GraphQL."""

#     event_id = str(uuid.uuid4())
#     user_id = str(uuid.uuid4())
#     inserted = None
#     updated = None

#     try:
#         inserted = await _event_insert(SchemaExecutor, event_id=event_id, name="pytest EventGQLModel mutation")
#         assert inserted["id"] == event_id
#         assert inserted["name"] == "pytest EventGQLModel mutation"
#         assert inserted["nameEn"] == "pytest EventGQLModel mutation EN"
#         assert inserted["description"] == "description for pytest EventGQLModel mutation"
#         assert inserted["place"] == "pytest graphql"
#         assert inserted["durationMinutes"] == 24 * 60

#         update_result = await SchemaExecutor(
#             query=f"""
#             mutation EventUpdate($event: EventUpdateGQLModel!) {{
#               eventUpdate(event: $event) {{
#                 ... on EventGQLModel {{
# {EVENT_FIELDS}
#                 }}
# {EVENT_ERROR_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={
#                 "event": {
#                     "id": event_id,
#                     "lastchange": inserted["lastchange"],
#                     "name": "pytest EventGQLModel mutation updated",
#                     "nameEn": "pytest EventGQLModel mutation updated EN",
#                     "description": "updated by EventGQLModel mutation test",
#                     "startdate": "2026-01-03T12:00:00",
#                     "enddate": "2026-01-03T14:30:00",
#                     "place": "pytest graphql updated",
#                 }
#             },
#         )
#         updated = assert_update(update_result)
#         assert updated["id"] == event_id
#         assert updated["name"] == "pytest EventGQLModel mutation updated"
#         assert updated["nameEn"] == "pytest EventGQLModel mutation updated EN"
#         assert updated["description"] == "updated by EventGQLModel mutation test"
#         assert updated["place"] == "pytest graphql updated"
#         assert updated["durationMinutes"] == 150
#         assert updated["durationHours"] == 2.5

#         ensure_result = await SchemaExecutor(
#             query=f"""
#             mutation EventEnsureInvitations($event: EventEnsureUserInvitationsModel!) {{
#               eventEnsureInvitations(event: $event) {{
#                 ... on EventGQLModel {{
# {EVENT_FIELDS}
#                 }}
# {EVENT_ERROR_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={
#                 "event": {
#                     "id": event_id,
#                     "userInvitations": [
#                         {
#                             "userId": user_id,
#                             "stateId": ORGANIZER_STATE_ID,
#                         }
#                     ],
#                 }
#             },
#         )
#         ensured = assert_update(ensure_result)
#         assert ensured["id"] == event_id
#         assert any(row["userId"] == user_id and row["stateId"] == ORGANIZER_STATE_ID for row in ensured["userInvitations"])

#         delete_result = await SchemaExecutor(
#             query=f"""
#             mutation EventDelete($event: EventDeleteGQLModel!) {{
#               eventDelete(event: $event) {{
# {EVENT_ERROR_FIELDS}
#               }}
#             }}
#             """,
#             variable_values={"event": {"id": event_id, "lastchange": ensured["lastchange"]}},
#         )
#         assert_delete(delete_result)
#         inserted = None
#         updated = None

#         deleted_read = await SchemaExecutor(
#             query="""
#             query EventById($id: UUID!) {
#               eventById(id: $id) {
#                 __typename
#                 id
#                 name
#                 lastchange
#               }
#             }
#             """,
#             variable_values={"id": event_id},
#         )
#         # load_with_loader returns an empty shell with the requested id when the
#         # record is not found.  The important contract here is that the deleted
#         # business data is no longer readable.
#         assert deleted_read.get("errors") is None
#         deleted = deleted_read.get("data", {}).get("eventById")
#         assert deleted is None or deleted.get("name") is None

#     finally:
#         if updated is not None:
#             await _event_delete(SchemaExecutor, event_id=event_id, lastchange=updated.get("lastchange"))
#         elif inserted is not None:
#             await _event_delete(SchemaExecutor, event_id=event_id, lastchange=inserted.get("lastchange"))
