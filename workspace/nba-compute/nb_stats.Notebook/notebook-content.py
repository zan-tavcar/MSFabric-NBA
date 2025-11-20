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

def game_stats(gameid):
    import requests
    from pyspark.sql.functions import col, from_json
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

    # Define schema for the `data` array
    data_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("min", StringType(), True),
        StructField("fgm", IntegerType(), True),
        StructField("fga", IntegerType(), True),
        StructField("fg_pct", StringType(), True),
        StructField("fg3m", IntegerType(), True),
        StructField("fg3a", IntegerType(), True),
        StructField("fg3_pct", StringType(), True),
        StructField("ftm", IntegerType(), True),
        StructField("fta", IntegerType(), True),
        StructField("ft_pct", StringType(), True),
        StructField("oreb", IntegerType(), True),
        StructField("dreb", IntegerType(), True),
        StructField("reb", IntegerType(), True),
        StructField("ast", IntegerType(), True),
        StructField("stl", IntegerType(), True),
        StructField("blk", IntegerType(), True),
        StructField("turnover", IntegerType(), True),
        StructField("pf", IntegerType(), True),
        StructField("pts", IntegerType(), True),
        StructField("player", StructType([
            StructField("id", IntegerType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("position", StringType(), True),
            StructField("height", StringType(), True),
            StructField("weight", StringType(), True),
            StructField("jersey_number", StringType(), True),
            StructField("college", StringType(), True),
            StructField("country", StringType(), True),
            StructField("draft_year", IntegerType(), True),
            StructField("draft_round", IntegerType(), True),
            StructField("draft_number", IntegerType(), True),
            StructField("team_id", IntegerType(), True)
        ]), True),
        StructField("team", StructType([
            StructField("id", IntegerType(), True),
            StructField("conference", StringType(), True),
            StructField("division", StringType(), True),
            StructField("city", StringType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("abbreviation", StringType(), True)
        ]), True),
        StructField("game", StructType([
            StructField("id", IntegerType(), True),
            StructField("date", StringType(), True),
            StructField("season", IntegerType(), True),
            StructField("status", StringType(), True),
            StructField("period", IntegerType(), True),
            StructField("time", StringType(), True),
            StructField("postseason", BooleanType(), True),
            StructField("home_team_score", IntegerType(), True),
            StructField("visitor_team_score", IntegerType(), True),
            StructField("home_team_id", IntegerType(), True),
            StructField("visitor_team_id", IntegerType(), True)
        ]), True)
    ])
    
    df = spark.createDataFrame([], schema=data_schema)
    df = df.withColumn("playerid", col("player.id"))
    df = df.withColumn("teamid", col("team.id"))
    df = df.withColumn("gameid", col("game.id"))
    df = df.drop("player")
    df = df.drop("team")
    df = df.drop("game")

    cursor = 0

    while True:
        url = f"https://api.balldontlie.io/v1/stats?cursor={cursor}&game_ids[]={gameid}"
        headers = {
            "Authorization": f"{ApiKey}"  
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                new_df = spark.createDataFrame(response.json()["data"], schema=data_schema)
                new_df = new_df.withColumn("playerid", col("player.id"))
                new_df = new_df.withColumn("teamid", col("team.id"))
                new_df = new_df.withColumn("gameid", col("game.id"))
                new_df = new_df.drop("player")
                new_df = new_df.drop("team")
                new_df = new_df.drop("game")

                df = df.union(new_df)
                next_cursor = response.json()["meta"]["next_cursor"]
                cursor = next_cursor
            except:
                break
        else:
            break

    return df


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType
from pyspark.sql.functions import col

# Define the schema
data_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("min", StringType(), True),
    StructField("fgm", IntegerType(), True),
    StructField("fga", IntegerType(), True),
    StructField("fg_pct", StringType(), True),
    StructField("fg3m", IntegerType(), True),
    StructField("fg3a", IntegerType(), True),
    StructField("fg3_pct", StringType(), True),
    StructField("ftm", IntegerType(), True),
    StructField("fta", IntegerType(), True),
    StructField("ft_pct", StringType(), True),
    StructField("oreb", IntegerType(), True),
    StructField("dreb", IntegerType(), True),
    StructField("reb", IntegerType(), True),
    StructField("ast", IntegerType(), True),
    StructField("stl", IntegerType(), True),
    StructField("blk", IntegerType(), True),
    StructField("turnover", IntegerType(), True),
    StructField("pf", IntegerType(), True),
    StructField("pts", IntegerType(), True),
    StructField("playerid", IntegerType(), True),  # Extracted from player.id
    StructField("teamid", IntegerType(), True),    # Extracted from team.id
    StructField("gameid", IntegerType(), True)     # Extracted from game.id
])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read the games and gamelines Delta tables from abfss paths
games_df = spark.read.format("delta").load(f"{lakehouse_abfss}/Tables/bronze/games")
try:
    gamelines_df = spark.read.format("delta").load(f"{lakehouse_abfss}/Tables/bronze/gamelines")
except Exception:
    gamelines_df = spark.createDataFrame([], schema="gameid STRING")

# Filter games where time == 'Final'
final_games_df = games_df.filter(games_df["time"] == "Final").select("id")
game_ids_header = final_games_df.rdd.flatMap(lambda x: x).collect()

# Collect all gameid values from gamelines
game_ids_lines = gamelines_df.select("gameid").rdd.flatMap(lambda x: x).collect()

# Convert to sets and compute the difference
game_ids_header_set = set(game_ids_header)
game_ids_lines_set = set(game_ids_lines)
game_ids_to_process = game_ids_header_set - game_ids_lines_set


schema = "bronze"
table = "gamelines"
path = f"{lakehouse_abfss}/Tables/{schema}/{table}"

for games in game_ids_to_process:
    gamestats_df = game_stats(games)
    print(f"Processing game: {games}")
    gamestats_df.write.format("delta").mode("append").save(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
