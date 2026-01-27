import aiohttp
import asyncio
import os
import sys
import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    client = TestClient(main.app, raise_server_exceptions=False)
    return client


async def getToken(
    username, 
    password,
    keyurl = "http://localhost:33001/oauth/login3"
):
    
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            print(resp.status)
            keyJson = await resp.json()
            print(keyJson)

        payload = {"key": keyJson["key"], "username": username, "password": password}
        async with session.post(keyurl, json=payload) as resp:
            print(resp.status)
            tokenJson = await resp.json()
            print(tokenJson)
    return tokenJson.get("token", None)
            

def createFederationClient(
    username="john.newbie@world.com", 
    password="john.newbie@world.com",
    gqlurl="http://localhost:33001/api/gql"
):
    token = None
    async def post(query, variables):
        nonlocal token
        if token is None:
            token = await getToken(username, password)

        payload = {"query": query, "variables": variables}
        # headers = {"Authorization": f"Bearer {token}"}
        cookies = {'authorization': token}
        async with aiohttp.ClientSession() as session:
            # print(headers, cookies)
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                # print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return text
                else:
                    response = await resp.json()
                    return response
    return post 

def is_json(responsejson):
    assert isinstance(responsejson, dict), f"GQL response is not a dict: {responsejson}"
    return True

def has_no_errors(resposejson):
    assert "errors" not in resposejson, f"GQL response has errors: {resposejson['errors']}"
    return True

def has_data_field(responsejson):
    assert "data" in responsejson, f"GQL response has no data field: {responsejson}"
    return True

def basic_checks(responsejson):
    is_json(responsejson)
    has_no_errors(responsejson)
    has_data_field(responsejson)
    return True

def data_has_field(responsejson, fieldname):
    data = responsejson.get("data", {})
    assert fieldname in data, f"GQL response data has no field '{fieldname}': {data}"
    return True

# ============================================
# GraphQL Queries and Mutations for Projects
# ============================================

PROJECT_CREATE = """
mutation projectInsert($name: String!, $description: String, $startdate: DateTime, $enddate: DateTime, $rbacobjectId: UUID!, $isdone: Boolean) {
  projectInsert(
    project: {name: $name, description: $description, startdate: $startdate, enddate: $enddate, rbacobjectId: $rbacobjectId, isdone: $isdone}
  ) {
    ... on ProjectGQLModel {
      __typename
      id
      lastchange
      name
      description
      startdate
      enddate
      isdone
    }
    ... on InsertError {
      __typename
      code
      location
      failed
      input
      msg
    }
  }
}
"""

PROJECT_READ = """
query projectById($id: UUID!) {
  projectById(id: $id) {
    __typename
    id
    lastchange
    name
    description
    startdate
    enddate
    isdone
  }
}
"""

PROJECT_PAGE = """
query projectPage {
  projectPage {
    id
    name
    description
    isdone
  }
}
"""

PROJECT_UPDATE = """
mutation projectUpdate($id: UUID!, $lastchange: DateTime!, $name: String, $description: String, $startdate: DateTime, $enddate: DateTime, $isdone: Boolean) {
  projectUpdate(
    project: {id: $id, lastchange: $lastchange, name: $name, description: $description, startdate: $startdate, enddate: $enddate, isdone: $isdone}
  ) {
    ... on ProjectGQLModel {
      __typename
      id
      lastchange
      name
      description
      startdate
      enddate
      isdone
    }
    ... on ProjectGQLModelUpdateError {
      __typename
      code
      location
      failed
      input
      msg
    }
  }
}
"""

PROJECT_DELETE = """
mutation projectDelete($id: UUID!, $lastchange: DateTime!) {
  projectDelete(project: {id: $id, lastchange: $lastchange}) {
    ... on ProjectGQLModelDeleteError {
      __typename
      failed
      input
      msg
    }
  }
}
"""

# ============================================
# Color codes for terminal output
# ============================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_test(name, status, details=""):
    """Print colored test result"""
    if status == "PASS":
        symbol = "✓"
        color = Colors.GREEN
    elif status == "FAIL":
        symbol = "✗"
        color = Colors.RED
    else:  # INFO
        symbol = "ℹ"
        color = Colors.CYAN
    
    print(f"{color}{Colors.BOLD}[{symbol}]{Colors.RESET} {color}{name}{Colors.RESET}", end="")
    if details:
        print(f" {Colors.RESET}→ {details}", end="")
    print()


def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.RESET}\n")

# ============================================
# CRUD Test Suite
# ============================================

# Default credentials and IDs
DEFAULT_USERNAME = "john.newbie@world.com"
DEFAULT_PASSWORD = "john.newbie@world.com"
GQL_PORT = "33001"
UNIVERSITY_ADMIN_RBAC_ID = "d75d64a4-bf5f-43c5-9c14-8fda7aff6c09"

async def run_mutation(mutation_string, variables, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
    """Execute a mutation with proper error handling"""
    # Convert datetime objects to ISO format strings for JSON serialization
    converted_vars = {}
    for key, value in variables.items():
        if isinstance(value, datetime.datetime):
            converted_vars[key] = value.isoformat()
        else:
            converted_vars[key] = value
    
    client = createFederationClient(username, password)
    result = await client(mutation_string, converted_vars)
    basic_checks(result)
    return result


async def test_project_crud():
    """Test Project CREATE, READ, UPDATE, DELETE operations"""
    print_section("PROJECT CRUD TESTS")
    
    project_id = None
    project_lastchange = None
    
    try:
        # ========== KROK 2: PROJECT CREATE ==========
        # Vytvoř nový projekt s parametry: name, description, dates, rbacobjectId, isdone
        # Ověř, že jsou vráceny všechna pole včetně automaticky generovaného ID a lastchange
        # ===== CREATE =====
        print_test("Project CREATE", "INFO", "Creating a new project...")
        
        create_vars = {
            "name": "Test Project",
            "description": "This is a test project for CRUD operations",
            "startdate": datetime.datetime(2026, 1, 26),
            "enddate": datetime.datetime(2026, 12, 31),
            "rbacobjectId": UNIVERSITY_ADMIN_RBAC_ID,
            "isdone": False
        }
        
        result = await run_mutation(PROJECT_CREATE, create_vars)
        project_data = result["data"]["projectInsert"]
        
        assert project_data["__typename"] == "ProjectGQLModel", f"Wrong type returned: {project_data['__typename']}"
        assert project_data["name"] == "Test Project", "Name mismatch"
        assert project_data["isdone"] == False, "isdone should be False"
        
        project_id = project_data["id"]
        project_lastchange = project_data["lastchange"]
        
        print_test("Project CREATE", "PASS", f"id={project_id[:8]}..., name='{project_data['name']}', isdone={project_data['isdone']}")
    
        # ========== KROK 3: PROJECT READ ==========
        # Načti vytvořený projekt z DB pomocí jeho ID
        # Ověř, že všechna vrácená pole odpovídají datům, která byla vložena v CREATE
        # ===== READ =====
        print_test("Project READ", "INFO", f"Reading project {project_id[:8]}...")
        client = createFederationClient()
        read_result = await client(PROJECT_READ, {"id": project_id})
        basic_checks(read_result)
        
        read_project = read_result["data"]["projectById"]
        assert read_project["id"] == project_id, "ID mismatch"
        assert read_project["name"] == "Test Project", "Name mismatch on read"
        assert read_project["isdone"] == False, "Project should not be done"
        
        details = f"name='{read_project['name']}', description='{read_project.get('description', 'N/A')[:30]}...', isdone={read_project['isdone']}"
        print_test("Project READ", "PASS", details)
    
        # ========== KROK 4: PROJECT UPDATE ==========
        # Aktualizuj projekt: změní se name, description, dates a isdone (False -> True)
        # DŮLEŽITÉ: Musíš poslat správný lastchange z READ kroku, jinak server odmítne update
        # Ověř, že se všechna pole skutečně změnila v DB
        # ===== UPDATE =====
        print_test("Project UPDATE", "INFO", "Updating project...")
        update_vars = {
            "id": project_id,
            "lastchange": project_lastchange,
            "name": "Updated Test Project",
            "description": "Updated description for the project",
            "startdate": datetime.datetime(2026, 2, 1),
            "enddate": datetime.datetime(2026, 11, 30),
            "isdone": True
        }
        
        update_result = await run_mutation(PROJECT_UPDATE, update_vars)
        updated_project = update_result["data"]["projectUpdate"]
        
        assert updated_project["__typename"] == "ProjectGQLModel", "Wrong type on update"
        assert updated_project["id"] == project_id, "ID changed after update"
        assert updated_project["name"] == "Updated Test Project", "Name not updated"
        assert updated_project["description"] == "Updated description for the project", "Description not updated"
        assert updated_project["isdone"] == True, "isdone should be True"
        
        project_lastchange = updated_project["lastchange"]
        
        print_test("Project UPDATE", "PASS", f"name: 'Test Project' → '{updated_project['name']}', isdone: False → {updated_project['isdone']}")
    
        # ========== KROK 5: PROJECT UPDATE (STALE DATA TEST) ==========
        # Toto je TEST OPTIMISTICKÉHO UZAMYKÁNÍ (optimistic locking)
        # Pokus se updatovat projekt se ŠPATNÝM lastchange (z roku 2020)
        # Server MUSÍ odmítnout s chybou ProjectGQLModelUpdateError
        # Tím se zabraňuje konfliktům když dvě operace zkoušejí updatovat stejný záznam
        # ===== UPDATE with wrong lastchange (should fail) =====
        print_test("Project UPDATE (stale data)", "INFO", "Testing with wrong lastchange...")
        bad_update_vars = {
            "id": project_id,
            "lastchange": "2020-01-01T00:00:00",  # Wrong lastchange
            "name": "This should fail"
        }
        
        bad_result = await run_mutation(PROJECT_UPDATE, bad_update_vars)
        bad_update = bad_result["data"]["projectUpdate"]
        
        assert bad_update["__typename"] == "ProjectGQLModelUpdateError", f"Should return ProjectGQLModelUpdateError, got {bad_update['__typename']}"
        assert bad_update["failed"] == True, "Should have failed flag"
        
        print_test("Project UPDATE (stale data)", "PASS", f"Correctly rejected: {bad_update['msg'][:50]}...")
        
    finally:
        # ========== KROK 6: PROJECT DELETE ==========
        # Smaž projekt - DŮLEŽITÉ: Je v finally bloku!
        # To znamená, že se spustí VŽDYCKY, i když některý z testů výše selhaje
        # Tím se zajistí čištění DB a prevence sirotčích záznamů
        # ===== DELETE (cleanup always runs) =====
        if project_id and project_lastchange:
            print_test("Project DELETE", "INFO", f"Deleting project {project_id[:8]}...")
            delete_vars = {"id": project_id, "lastchange": project_lastchange}
            
            delete_result = await run_mutation(PROJECT_DELETE, delete_vars)
            del_response = delete_result["data"]["projectDelete"]
            
            if del_response is None:
                print_test("Project DELETE", "PASS", f"Project (id={project_id[:8]}...) deleted successfully")
            else:
                assert del_response.get("failed") == False or del_response.get("failed") is None, "Delete should succeed"
                print_test("Project DELETE", "PASS", f"Project (id={project_id[:8]}...) deleted")


async def main():
    """Run all CRUD tests"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}")
    print(f"{'  GRAPHQL CRUD TEST SUITE':^60}")
    print(f"{'='*60}{Colors.RESET}\n")
    
    # ========== KROK 1: PRE-TEST CHECK ==========
    # Ověř, že server běží a spočítej počáteční počet projektů
    # Toto slouží jako baseline pro ověření čištění DB na konci
    print_test("Pre-test Check", "INFO", "Checking initial database state...")
    client = createFederationClient()
    initial_projects = await client(PROJECT_PAGE, {})
    
    # Validate responses
    if initial_projects is None:
        print_test("Pre-test Check", "FAIL", "PROJECT_PAGE query returned None - server might not be running or query has syntax error")
        raise Exception("PROJECT_PAGE query failed")
    
    try:
        basic_checks(initial_projects)
    except AssertionError as e:
        print_test("Pre-test Check", "FAIL", f"PROJECT_PAGE response validation failed: {str(e)}")
        print(f"Response: {initial_projects}")
        raise
    
    initial_project_count = len(initial_projects.get("data", {}).get("projectPage", [])) if initial_projects else 0
    
    print_test("Pre-test Check", "PASS", f"Initial state: {initial_project_count} projects")
    
    try:
        await test_project_crud()
        
        # ========== KROK 7: POST-TEST CHECK ==========
        # Spustí PROJECT_PAGE query znovu a porovná počet projektů
        # Počet by měl být STEJNÝ jako na začátku (initial_project_count)
        # Pokud je jiný, znamená to, že DELETE v kroku 6 neprošel a zůstaly sirotčí záznamy
        # Check final database state
        print_test("Post-test Check", "INFO", "Verifying database cleanup...")
        final_projects = await client(PROJECT_PAGE, {})
        
        if final_projects is None:
            print_test("Post-test Check", "FAIL", "Final state queries returned None")
            raise Exception("Final state queries failed")
        
        try:
            basic_checks(final_projects)
        except AssertionError as e:
            print_test("Post-test Check", "FAIL", f"Final state validation failed: {str(e)}")
            raise
        
        final_project_count = len(final_projects.get("data", {}).get("projectPage", [])) if final_projects else 0
        
        if final_project_count == initial_project_count:
            print_test("Post-test Check", "PASS", f"Database clean: {final_project_count} projects")
        else:
            print_test("Post-test Check", "FAIL", f"Database NOT clean! Projects: {final_project_count} (expected {initial_project_count})")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*60}")
        print(f"{'  ALL TESTS PASSED ✓':^60}")
        print(f"{'='*60}{Colors.RESET}\n")
        
    except AssertionError as e:
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*60}")
        print(f"  TEST FAILED ✗")
        print(f"{'='*60}")
        print(f"{Colors.RED}Error: {e}{Colors.RESET}\n")
        raise
    except Exception as e:
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*60}")
        print(f"  UNEXPECTED ERROR ✗")
        print(f"{'='*60}")
        print(f"{Colors.RED}Error: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        raise

    # Legacy test for backward compatibility
    result = await test_me_query()
    basic_checks(result)
    data_has_field(result, "result")
    print(result)

async def test_me_query():
    client = createFederationClient()
    result = await client("{result: projectPage{id created lastchange}}", {})
    return result

if __name__ == "__main__":
    asyncio.run(main())