from azure.identity import ClientSecretCredential
import os
import requests
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
tenant_id = os.environ["TENANT_ID"]
token_credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
branch = (
    os.getenv("GITHUB_REF_NAME")
).replace("refs/heads/", "").strip()

    
# Sample values for FabricWorkspace parameters
if branch == "dev":
    workspace_id = "08c998b5-75a3-4c85-9665-4a5cd6add41d"
    environment = "DEV"
elif branch == "prod":
    workspace_id = "2dedd6fb-8e30-4605-ae85-f2fc70c0c536"
    environment = "PROD"
else:
    raise ValueError("Invalid branch to deploy from")

repository = os.path.abspath("./workspace/nba-compute")
item_type_in_scope = ["Notebook"]


# -------------------------------------------------------
# Helper: Fabric REST API call setup
# -------------------------------------------------------
def get_fabric_headers():
    # Scope for Fabric REST API
    token = token_credential.get_token("https://api.fabric.microsoft.com/.default").token
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

# -------------------------------------------------------
# STEP 1: Delete nb_orchestration via Fabric REST API
# -------------------------------------------------------
print("Looking for 'nb_orchestration' notebook to delete via Fabric REST API...")

headers = get_fabric_headers()

# List items in the workspace (optionally filter by itemType=notebook)
list_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items?itemType=notebook"
resp = requests.get(list_url, headers=headers)
resp.raise_for_status()

items = resp.json().get("value", [])

nb_orchestration_id = None
for item in items:
    # displayName is the item name without the .Notebook suffix
    if item.get("displayName") == "nb_orchestration":
        nb_orchestration_id = item.get("id")
        break

if nb_orchestration_id:
    delete_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{nb_orchestration_id}"
    print(f"Deleting nb_orchestration (ID: {nb_orchestration_id})...")
    del_resp = requests.delete(delete_url, headers=headers)
    # 200 OK is success
    if del_resp.status_code == 200:
        print("nb_orchestration deleted successfully.")
    elif del_resp.status_code == 404:
        print("nb_orchestration not found at delete time (already removed?).")
    else:
        print(f"Failed to delete nb_orchestration, status {del_resp.status_code}, body: {del_resp.text}")
else:
    print("nb_orchestration not found in workspace — nothing to delete.")
    

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=environment,
    repository_directory=repository,
    item_type_in_scope=item_type_in_scope,
    token_credential=token_credential
)
# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)

# Unpublish all items defined in item_type_in_scope not found in repository

unpublish_all_orphan_items(target_workspace)





