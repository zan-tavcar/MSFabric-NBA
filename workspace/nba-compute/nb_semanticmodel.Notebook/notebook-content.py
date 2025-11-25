# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

%pip install semantic-link-labs --quiet
import sempy.fabric as fabric
import sempy_labs as labs

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run nb_config

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

DATASET_NAME   = semanticmodel_id
WORKSPACE_NAME = semanticmodel_ws   


labs.refresh_semantic_model(
    dataset=DATASET_NAME,
    workspace=WORKSPACE_NAME
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
