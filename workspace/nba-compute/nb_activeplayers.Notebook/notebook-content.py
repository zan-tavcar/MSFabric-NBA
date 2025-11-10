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


ApiKey =  mssparkutils.credentials.getSecret(
    'https://dataconsultingkeyvault.vault.azure.net/',      
    'balldontlie'
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col,from_json

player_schema = StructType([
    StructField("id", IntegerType(), True),  # Assuming "id" is always an integer.
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("position", StringType(), True),
    StructField("height", StringType(), True),  # Keep as String for formats like "6-2".
    StructField("weight", StringType(), True),  # Keep as String initially to handle non-numeric cases.
    StructField("jersey_number", StringType(), True),  # Some jersey numbers may have non-numeric characters.
    StructField("college", StringType(), True),
    StructField("country", StringType(), True),
    StructField("draft_year", StringType(), True),  # Initially String for non-standard values.
    StructField("draft_round", StringType(), True),
    StructField("draft_number", StringType(), True),
    StructField("team", StructType([  # Nested structure for "team".
        StructField("id", IntegerType(), True),
        StructField("conference", StringType(), True),
        StructField("division", StringType(), True),
        StructField("city", StringType(), True),
        StructField("name", StringType(), True),
        StructField("full_name", StringType(), True),
        StructField("abbreviation", StringType(), True)
    ]))
])



df = spark.createDataFrame([],schema = player_schema)
df = df.withColumn("team_id", col("team.id"))
df = df.drop("team")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
from pyspark.sql.functions import col,from_json

cursor = 0

while True:

    url = f"https://api.balldontlie.io/v1/players/active?cursor={cursor}&per_page=25"
    headers = {
        "Authorization": f"{ApiKey}"  
    }


    response = requests.get(url, headers=headers)
    if response.status_code == 200:

        try:
            new_df = spark.createDataFrame(response.json()["data"],schema = player_schema)
            new_df = new_df.withColumn("team_id", col("team.id"))
            new_df = new_df.drop("team")
            df = df.union(new_df)
            next_cursor = response.json()["meta"]["next_cursor"]
            cursor = next_cursor
        except:
            break

           






# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = "bronze"
table = "players"
path = f"{lakehouse_abfss}/Tables/{schema}/{table}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import concat, lit


df = df.withColumn("full_name",concat(df["first_name"], lit(" "), df["last_name"]))
df.distinct().write.format("delta").mode("overwrite").option("mergeSchema","true").save(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
