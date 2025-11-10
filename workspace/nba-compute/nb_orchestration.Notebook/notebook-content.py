# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": ""
# META     }
# META   }
# META }

# CELL ********************

from notebookutils import notebook

# Define the DAG
DAG = {
    "activities": [
        {
            "name": "nb_teams",
            "path": "nb_teams",
            "timeoutPerCellInSeconds": 3600 #90 is default LOL
        },
        {
            "name": "nb_activeplayers",
            "path": "nb_activeplayers",
            "timeoutPerCellInSeconds": 3600,
            "dependencies":["nb_teams"]
        },
            {
            "name": "nb_games",
            "path": "nb_games",
            "timeoutPerCellInSeconds": 3600,
            "dependencies":["nb_teams"]
        },
            {
            "name": "nb_stats",
            "path": "nb_stats",
            "timeoutPerCellInSeconds": 3600,
            "dependencies":["nb_games"]
        },            
        {
            "name": "nb_frontend",
            "path": "nb_frontend",
            "timeoutPerCellInSeconds": 3600,
            "dependencies":["nb_games"]
        }
    ],
    "concurrency":3,
    "timeoutInSeconds": 3600
}

# Execute the DAG
notebookutils.notebook.runMultiple(DAG, {"dispayDAGViaGraphViz":True})


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
