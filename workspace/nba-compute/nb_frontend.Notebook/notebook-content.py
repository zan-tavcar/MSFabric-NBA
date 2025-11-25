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

%run nb_config

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


from pyspark.sql.functions import *
from datetime import datetime, timedelta



# Define date range
start_date = datetime.strptime("2025-10-22", "%Y-%m-%d")
end_date = datetime.strptime("2026-01-31", "%Y-%m-%d")
days = (end_date - start_date).days + 1

# Create list of dates
date_list = [(start_date + timedelta(days=i),) for i in range(days)]

# Create DataFrame
df = spark.createDataFrame(date_list, ["date"])

#MaxDate from games
max_date = spark.read.format("delta").load(f"{lakehouse_abfss}/Tables/bronze/games")
max_date = max_date.filter(col("status") == "Final").\
            withColumn("MaxDate",col("date").cast("date")).\
            select("MaxDate").agg(max(col("MaxDate")).alias("MaxDate"))

# Add columns including string-formatted date
calendar_df = df.select(
    date_format("date", "yyyy-MM-dd").alias("date"),
    col("date").cast("date").alias("dateformat"),
    date_format("date", "yyyy MMM").alias("year_month"),
    date_format("date", "yyyyMM").alias("year_month_sort"),
    date_format("date", "MMM d").alias("date_label")).alias("calendar")\
.join(max_date.alias("max_date"), 
    on = col("max_date.MaxDate") == col("calendar.dateformat"),
    how="left")\
.withColumn("IsLastDay", expr("CASE WHEN MaxDate IS NOT NULL THEN 1 ELSE NULL END"))

# Write to Delta table
calendar_df.write.mode("overwrite").format("delta").save(f"{lakehouse_abfss}/Tables/dbo/calendar")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Metadata

# CELL ********************

from datetime import datetime

# format date like "Jun 12, 2024"
last_refresh = datetime.today().strftime("%b %d, %Y")

data = [
    ("Last Refresh", last_refresh),     
    ("Developer",    "Zan Tavcar"),
    ("Team",         "User Experience"),
    ("Version",      "1.0")
]

df_meta = spark.createDataFrame(data, ["Type", "Value"])

#df_meta.show(truncate=False)
df_meta.write.mode("overwrite").format("delta").save(f"{lakehouse_abfss}/Tables/dbo/metadata")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
