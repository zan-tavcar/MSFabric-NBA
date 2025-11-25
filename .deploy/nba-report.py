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
    workspace_id = "73bcbe0e-d40c-4a29-8362-004feeae0b56"
    environment = "DEV"
elif branch == "prod":
    workspace_id = "418466ca-14b2-4964-a18b-9c0828ea21fa"
    environment = "PROD"
else:
    raise ValueError("Invalid branch to deploy from")

repository = os.path.abspath("./workspace/nba-report")
item_type_in_scope = ["SemanticModel","Report"]

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

