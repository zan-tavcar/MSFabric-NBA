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


def games_on_date(date):
        import requests
        from pyspark.sql.functions import col,from_json
        from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

        # Define schema for the `data` array
        data_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("date", StringType(), True),
        StructField("season", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("period", IntegerType(), True),
        StructField("time", StringType(), True),
        StructField("postseason", BooleanType(), True),
        StructField("home_team_score", IntegerType(), True),
        StructField("visitor_team_score", IntegerType(), True),
        StructField("home_team", StructType([
            StructField("id", IntegerType(), True),
            StructField("conference", StringType(), True),
            StructField("division", StringType(), True),
            StructField("city", StringType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("abbreviation", StringType(), True)
        ])),
        StructField("visitor_team", StructType([
            StructField("id", IntegerType(), True),
            StructField("conference", StringType(), True),
            StructField("division", StringType(), True),
            StructField("city", StringType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("abbreviation", StringType(), True)
        ]))
    ])





        df = spark.createDataFrame([],schema = data_schema)
        df = df.withColumn("home_teamid", col("home_team.id"))
        df = df.withColumn("visitor_teamid", col("visitor_team.id"))
        df = df.drop("home_team")
        df = df.drop("visitor_team")

        cursor = 0

        while True:

            url = f"https://api.balldontlie.io/v1/games?cursor={cursor}&dates[]={date}"
            headers = {
                "Authorization": f"{ApiKey}"  
            }


            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                try:
                    new_df = spark.createDataFrame(response.json()["data"],schema = data_schema)
                    new_df = new_df.withColumn("home_teamid", col("home_team.id"))
                    new_df = new_df.withColumn("visitor_teamid", col("visitor_team.id"))
                    new_df = new_df.drop("home_team")
                    new_df = new_df.drop("visitor_team")
                    df = df.unionAll(new_df)
                    next_cursor = response.json()["meta"]["next_cursor"]
                    cursor = next_cursor
                except:
                    break
        return df

            






# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


def games_season(season):
        import requests
        from pyspark.sql.functions import col,from_json
        from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType

        # Define schema for the `data` array
        data_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("date", StringType(), True),
        StructField("season", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("period", IntegerType(), True),
        StructField("time", StringType(), True),
        StructField("postseason", BooleanType(), True),
        StructField("home_team_score", IntegerType(), True),
        StructField("visitor_team_score", IntegerType(), True),
        StructField("home_team", StructType([
            StructField("id", IntegerType(), True),
            StructField("conference", StringType(), True),
            StructField("division", StringType(), True),
            StructField("city", StringType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("abbreviation", StringType(), True)
        ])),
        StructField("visitor_team", StructType([
            StructField("id", IntegerType(), True),
            StructField("conference", StringType(), True),
            StructField("division", StringType(), True),
            StructField("city", StringType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("abbreviation", StringType(), True)
        ]))
    ])





        df = spark.createDataFrame([],schema = data_schema)
        df = df.withColumn("home_teamid", col("home_team.id"))
        df = df.withColumn("visitor_teamid", col("visitor_team.id"))
        df = df.drop("home_team")
        df = df.drop("visitor_team")

        cursor = 0

        while True:

            url = f"https://api.balldontlie.io/v1/games?cursor={cursor}&seasons[]={season}&per_page=25"
            headers = {
                "Authorization": f"{ApiKey}"  
            }


            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                try:
                    new_df = spark.createDataFrame(response.json()["data"],schema = data_schema)
                    new_df = new_df.withColumn("home_teamid", col("home_team.id"))
                    new_df = new_df.withColumn("visitor_teamid", col("visitor_team.id"))
                    new_df = new_df.drop("home_team")
                    new_df = new_df.drop("visitor_team")
                    df = df.unionAll(new_df)
                    next_cursor = response.json()["meta"]["next_cursor"]
                    response = response.json()["meta"]
                    print(response)
                    cursor = next_cursor
                    print(next_cursor)
                except:
                    break
        return df

            






# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from datetime import datetime, timedelta
from pyspark.sql import SparkSession

# Initialize Spark session if not already done
spark = SparkSession.builder.getOrCreate()

# Function to generate all dates between two dates
def generate_date_range(start_date, end_date):
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = []
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return date_list

start_date = "2025-10-22"
end_date = "2025-12-31"
dates = generate_date_range(start_date, end_date)

# Empty DataFrame to store results
final_df = None

# Iterate through each date and append results
for date in dates:
    try:
        # Call the games_on_date function for each date
        daily_df = games_on_date(date)
        
        # Append to the final DataFrame
        if final_df is None:
            final_df = daily_df
        else:
            final_df = final_df.unionAll(daily_df)
            
        print(f"Processed data for date: {date}")
    except Exception as e:
        print(f"Error processing date {date}: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Joining Teams data to gamelines table

# CELL ********************

# Load the Delta table from abfss path
teams_df = spark.read.format("delta").load(f"{lakehouse_abfss}/Tables/bronze/teams")

# Create hometeam transformation
hometeam = teams_df.selectExpr(
    "id as hometeam_id",
    "full_name as hometeam_fullname",
    "abbreviation as hometeam_abbreviation",
    "logo as hometeam_logo"
)

# Create awayteam transformation
awayteam = teams_df.selectExpr(
    "id as awayteam_id",
    "full_name as awayteam_fullname",
    "abbreviation as awayteam_abbreviation",
    "logo as awayteam_logo"
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col
df = final_df.join(hometeam, final_df.home_teamid == hometeam.hometeam_id) \
.join(awayteam, final_df.visitor_teamid == awayteam.awayteam_id) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = "bronze"
table = "games"
path = f"{lakehouse_abfss}/Tables/{schema}/{table}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.distinct().write.format("delta").mode("overwrite").save(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
