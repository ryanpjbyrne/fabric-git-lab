# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from pyspark.sql import functions as F

MIN_ROW_COUNT = 1
MAX_NULL_RATES = {
    "customer_id": 0.0,
    "customer_name": 0.05,
    "postcode": 0.05,
}

silver = spark.read.table("silver_customers")

metrics = silver.agg(
    F.count("*").alias("row_count"),
    F.avg(F.col("customer_id").isNull().cast("double")).alias("customer_id_null_rate"),
    F.avg(
        (F.col("customer_name").isNull() | (F.trim(F.col("customer_name")) == ""))
        .cast("double")
    ).alias("customer_name_null_rate"),
    F.avg(
        (F.col("postcode").isNull() | (F.trim(F.col("postcode")) == ""))
        .cast("double")
    ).alias("postcode_null_rate"),
).first()

results = {
    "row_count": metrics["row_count"],
    "null_rates": {
        column: metrics[f"{column}_null_rate"]
        for column in MAX_NULL_RATES
    },
}
print(f"silver_customers quality results: {results}")

failures = []
if results["row_count"] < MIN_ROW_COUNT:
    failures.append(
        f"row_count {results['row_count']} is below minimum {MIN_ROW_COUNT}"
    )

for column, maximum in MAX_NULL_RATES.items():
    rate = results["null_rates"][column]
    if rate is not None and rate > maximum:
        failures.append(
            f"{column} null rate {rate:.2%} exceeds maximum {maximum:.2%}"
        )

if failures:
    raise ValueError("silver_customers quality checks failed: " + "; ".join(failures))

print("silver_customers quality checks passed")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
