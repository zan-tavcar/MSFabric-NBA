# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# ## Lakehouse Endpoint

# CELL ********************

config = {
    "dev": {
        "workspace_id": "edb11fd0-a25c-4817-8918-b9d74945988c",
        "workspace_name": "github-nba-storage-dev",
        "lakehouse_name": "NBA_Lakehouse"
    },
    "prod": {
        "workspace_id": "b87c2c54-c90d-4f6d-8fe4-c3a87cc7eb8c",
        "workspace_name": "github-nba-storage-prod",
        "lakehouse_name": "NBA_Lakehouse"
    }
}
fabric_endpoint = "abfss://{}@onelake.dfs.fabric.microsoft.com/{}.Lakehouse/"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

env = mssparkutils.env.getWorkspaceName()
env = env.split("-")[-1]

workspace_name = config[env]["workspace_name"]
lakehouse_name = config[env]["lakehouse_name"]

# Format the string with real values
lakehouse_abfss = fabric_endpoint.format(workspace_name, lakehouse_name)
print(lakehouse_abfss)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## SemanticModel Endpoint

# CELL ********************

config = {
    "dev": {
        "workspace_id": "73bcbe0e-d40c-4a29-8362-004feeae0b56",
        "workspace_name": "github-nba-report-dev",
        "semanticmodel_id": "9b8c3db5-fc10-4066-be00-ce8bd97e1923"
    },
    "prod": {
        "workspace_id": "418466ca-14b2-4964-a18b-9c0828ea21fa",
        "workspace_name": "github-nba-report-prod",
        "semanticmodel_id": "f66bb606-1ce0-4e63-8f6f-d5d7e7a94ac33"
    }
}

env = mssparkutils.env.getWorkspaceName()
env = env.split("-")[-1]
semanticmodel_ws = config[env]["workspace_id"]
semanticmodel_id = config[env]["semanticmodel_id"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
