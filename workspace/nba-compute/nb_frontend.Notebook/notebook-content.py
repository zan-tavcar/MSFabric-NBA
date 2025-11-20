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

# Set path to the folder containing CSV files
folder_path = f"{lakehouse_abfss}/Files/DummyFiles/"

# List of CSV files (based on your screenshot)
csv_files = [
    "Avatar.csv",
    "Images.csv",
    "Metadata.csv",
    "Pages.csv",
    "People.csv",
    "Slicers.csv",
    "Slideover.csv"
]

# Read each CSV and save as Delta table in dbo schema
for file in csv_files:
    table_name = file.replace(".csv", "").lower()
    csv_path = f"{folder_path}{file}"

    # Read CSV using semicolon delimiter
    df = spark.read.format("csv").option("header", "true").option("sep", ";").load(csv_path)

    # Rename columns to remove spaces
    for col_name in df.columns:
        df = df.withColumnRenamed(col_name, col_name.replace(" ", ""))

    # Write to Delta table in dbo schema
    df.write.mode("overwrite").format("delta").save(f"{lakehouse_abfss}/Tables/dbo/{table_name}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


from pyspark.sql.functions import col, date_format
from datetime import datetime, timedelta



# Define date range
start_date = datetime.strptime("2025-10-22", "%Y-%m-%d")
end_date = datetime.strptime("2026-01-31", "%Y-%m-%d")
days = (end_date - start_date).days + 1

# Create list of dates
date_list = [(start_date + timedelta(days=i),) for i in range(days)]

# Create DataFrame
df = spark.createDataFrame(date_list, ["date"])

# Add columns including string-formatted date
calendar_df = df.select(
    date_format("date", "yyyy-MM-dd").alias("date"),
    date_format("date", "yyyy MMM").alias("year_month"),
    date_format("date", "yyyyMM").alias("year_month_sort"),
    date_format("date", "MMM d").alias("date_label")
)

# Write to Delta table
calendar_df.write.mode("overwrite").format("delta").save(f"{lakehouse_abfss}/Tables/dbo/calendar")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
