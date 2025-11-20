# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

config = {
    "dev": {
        "workspace_id": "edb11fd0-a25c-4817-8918-b9d74945988c",
        "workspace_name": "github-nba-storage-dev",
        "lakehouse_name": "NBA_Lakehouse"
    },
    "prod": {
        "workspace_id": "dc1861de-0007-40e4-aaa9-7c1757a50069",
        "workspace_name": "nba3-storage-prod",
        "lakehouse_name": "lh_NBA"
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
