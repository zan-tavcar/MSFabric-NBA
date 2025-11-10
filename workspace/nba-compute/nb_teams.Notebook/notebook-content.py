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

# MARKDOWN ********************


# MARKDOWN ********************

# # Balldontlie API
# 
# 
# 
# **API Documentation**: https://docs.balldontlie.io/#nba-api
# 
# **Subscription Tier**: Free
# 


# CELL ********************

%run nb_config

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run nb_conn

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema explicitly
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("conference", StringType(), True),
    StructField("division", StringType(), True),
    StructField("city", StringType(), True),
    StructField("name", StringType(), True),
    StructField("full_name", StringType(), True),
    StructField("abbreviation", StringType(), True),
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests

from pyspark.sql.functions import col



url = "https://api.balldontlie.io/v1/teams"
headers = {
    "Authorization": f"{ApiKey}"  
}

response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print(response.json())  # Prints the JSON response
else:
    print(f"Error: {response.status_code}, {response.text}")

df = spark.createDataFrame(response.json()["data"], schema = schema)
df = df.filter(df.division != '')



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import when, lit, concat

# Add a new column with conditional logic for the logo URL
df = df.withColumn(
    "logo",
    concat(
        lit("https://a.espncdn.com/i/teamlogos/nba/500/"),
        when(df.abbreviation == "UTA", lit("UTH"))
        .when(df.abbreviation == "NOP", lit("NO"))
        .otherwise(df.abbreviation),
        lit(".png")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = "bronze"
table = "teams"
path = f"{lakehouse_abfss}/Tables/{schema}/{table}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").mode("overwrite").option("mergeSchema","true").save(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
