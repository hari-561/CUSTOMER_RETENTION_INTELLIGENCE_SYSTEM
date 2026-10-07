import pandas as pd


# =========================================================
# 1. Check NULL rate
# =========================================================

def check_null_rate(df, col, threshold):
    null_rate = df[col].isna().mean() * 100

    passed = null_rate <= threshold

    return {
        "check_name": f"Null rate - {col}",
        "status": "PASS" if passed else "FAIL",
        "value_found": round(null_rate, 2),
        "threshold": threshold,
        "severity": "CRITICAL"
    }


# =========================================================
# 2. Check value range
# =========================================================

def check_value_range(df, col, min_value, max_value=None):

    min_found = df[col].min()
    max_found = df[col].max()

    if max_value is None:
        passed = min_found >= min_value

        threshold = {
            "min": min_value
        }

    else:
        passed = (
            min_found >= min_value
            and max_found <= max_value
        )

        threshold = {
            "min": min_value,
            "max": max_value
        }

    return {
        "check_name": f"Value range - {col}",
        "status": "PASS" if passed else "FAIL",
        "value_found": {
            "min": min_found,
            "max": max_found
        },
        "threshold": threshold,
        "severity": "CRITICAL"
    }


# =========================================================
# 3. Check allowed values
# =========================================================

def check_allowed_values(df, col, allowed_set):

    actual_values = set(
        df[col].dropna().unique()
    )

    invalid_values = actual_values - set(allowed_set)

    passed = len(invalid_values) == 0

    return {
        "check_name": f"Allowed values - {col}",
        "status": "PASS" if passed else "FAIL",
        "value_found": sorted(
            list(actual_values)
        ),
        "invalid_values": sorted(
            list(invalid_values)
        ),
        "threshold": sorted(
            list(allowed_set)
        ),
        "severity": "CRITICAL"
    }


# =========================================================
# 4. Check row count
# =========================================================

def check_row_count(df, expected_min):

    actual_count = len(df)

    passed = actual_count >= expected_min

    return {
        "check_name": "Row count",
        "status": "PASS" if passed else "FAIL",
        "value_found": actual_count,
        "threshold": expected_min,
        "severity": "CRITICAL"
    }


# =========================================================
# 5. Check duplicates
# =========================================================

def check_no_duplicates(df, key_col):

    duplicate_count = df[key_col].duplicated().sum()

    passed = duplicate_count == 0

    return {
        "check_name": f"No duplicates - {key_col}",
        "status": "PASS" if passed else "FAIL",
        "value_found": int(duplicate_count),
        "threshold": 0,
        "severity": "CRITICAL"
    }


# =========================================================
# 6. Check churn distribution
# =========================================================

def check_churn_distribution(df):

    distribution = (
        df["churn"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
        .to_dict()
    )

    return {
        "check_name": "Churn distribution",
        "status": "PASS",
        "value_found": distribution,
        "threshold": "Informational",
        "severity": "WARNING"
    }