from azure.identity import ClientSecretCredential
import os
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
# Delete nb_orchestration first - there is bug in fabric-cicd (check #540 issue in their repo). This code below is temporary
print("Looking for 'nb_orchestration' to delete...")

items = target_workspace.fabric_api_client.get_items(workspace_id)

for item in items:
    # Item names do NOT include extension in API
    if item.get("displayName") == "nb_orchestration":
        item_id = item["id"]
        print(f"Deleting nb_orchestration (ID: {item_id})...")
        target_workspace.fabric_api_client.delete_item(workspace_id, item_id)
        break
else:
    print("nb_orchestration not found — nothing to delete.")
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


