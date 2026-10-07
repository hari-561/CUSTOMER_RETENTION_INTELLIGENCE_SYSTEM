import json
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(".."))
from phase1.cleanermodel import customer_cleaner

from quality_checks import (
    check_null_rate,
    check_value_range,
    check_allowed_values,
    check_row_count,
    check_no_duplicates,
    check_churn_distribution
)


CSV_PATH = "data/landing/WA_Fn-UseC_-Telco-Customer-Churn.csv"

REPORT_PATH = "data/logs/quality_report.json"



def convert_numpy_types(obj):

    if hasattr(obj, "item"):
        return obj.item()

    if isinstance(obj, dict):
        return {
            key: convert_numpy_types(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            convert_numpy_types(value)
            for value in obj
        ]

    return obj



# =========================================================
# Load CSV
# =========================================================

df = pd.read_csv(CSV_PATH)


# =========================================================
# Clean
# =========================================================

cleaner = customer_cleaner(df)

cleaned_df = cleaner.clean()


# =========================================================
# Rename customer ID
# =========================================================

if "customer_i_d" in cleaned_df.columns:

    cleaned_df = cleaned_df.rename(
        columns={
            "customer_i_d": "customer_id"
        }
    )


# =========================================================
# Run quality checks
# =========================================================

results = []


# 220. NULL checks

results.append(
    check_null_rate(
        cleaned_df,
        "monthly_charges",
        0
    )
)

results.append(
    check_null_rate(
        cleaned_df,
        "tenure",
        0
    )
)


# 221. Range checks

results.append(
    check_value_range(
        cleaned_df,
        "tenure",
        min_value=0,
        max_value=100
    )
)

results.append(
    check_value_range(
        cleaned_df,
        "monthly_charges",
        min_value=0,
        max_value=True
    )
)


# 222. Allowed contract values

results.append(
    check_allowed_values(
        cleaned_df,
        "contract",
        {
            "Month-to-month",
            "One year",
            "Two year"
        }
    )
)


# 223. Row count

results.append(
    check_row_count(
        cleaned_df,
        7000
    )
)


# 224. Duplicate customer ID

results.append(
    check_no_duplicates(
        cleaned_df,
        "customer_id"
    )
)


# Churn distribution

results.append(
    check_churn_distribution(
        cleaned_df
    )
)


# =========================================================
# Print quality report
# =========================================================

print("\n================================")
print("DATA QUALITY REPORT")
print("================================")

for result in results:

    print(
        f"{result['status']:4} | "
        f"{result['check_name']} | "
        f"Value: {result['value_found']} | "
        f"Threshold: {result['threshold']}"
    )


# =========================================================
# Save JSON report
# =========================================================

with open(REPORT_PATH, "w") as f:

    json.dump(
        convert_numpy_types(results),
        f,
        indent=4
    )

print(
    f"\nQuality report saved to: "
    f"{REPORT_PATH}"
)


# =========================================================
# 226. Stop on CRITICAL failures
# =========================================================

critical_failures = [
    result
    for result in results
    if (
        result["severity"] == "CRITICAL"
        and result["status"] == "FAIL"
    )
]


if critical_failures:

    print("\nCRITICAL QUALITY CHECK FAILED!")

    for failure in critical_failures:

        print(
            f"FAIL: {failure['check_name']} "
            f"| Value: {failure['value_found']} "
            f"| Threshold: {failure['threshold']}"
        )

    raise RuntimeError(
        "Pipeline stopped because "
        "critical data quality checks failed."
    )


# =========================================================
# 227. Log WARNING failures
# =========================================================

warnings = [
    result
    for result in results
    if (
        result["severity"] == "WARNING"
        and result["status"] == "FAIL"
    )
]


for warning in warnings:

    print(
        f"WARNING: {warning['check_name']} "
        f"| Value: {warning['value_found']} "
        f"| Threshold: {warning['threshold']}"
    )


print("\nAll critical quality checks passed.")
print("Pipeline can continue.")