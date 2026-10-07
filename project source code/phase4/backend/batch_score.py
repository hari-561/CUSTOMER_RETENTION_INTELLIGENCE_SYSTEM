import pandas as pd
from datetime import datetime

from sqlalchemy import text


from predict import predict_churn

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:root@localhost:3306/cris")


def score_customer(row):
    return predict_churn(
        tenure=row["tenure"],
        monthly_charges=row["monthly_charges"],
        contract_type=row["contract_type"],
        service_count=row["services_count"],
        internet_service=row["internet_service"]
    )




query = """
 select a.*,b.internet_service 
 from customer_ml_features a 
 join stg_customer_raw b on a.customer_id = b.customer_id ;
"""

df = pd.read_sql(
    query,
    engine
)

print("Customer ML features loaded successfully.")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


required_columns = [
    "customer_id",
    "tenure",
    "monthly_charges",
    "contract_type",
    "services_count",
    "internet_service"    
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

# if missing_columns:
#     raise ValueError(
#         f"Missing required columns: {missing_columns}"
#     )

print("All required columns are present.")



predictions = df.apply(
    score_customer,
    axis=1
)

print("Prediction completed.")

print("\nFirst 5 predictions:")
print(predictions.head())


prediction_df = pd.DataFrame(
    predictions.tolist(),
    index=df.index
)

df["risk_score"] = prediction_df["risk_score"]
df["prediction"] = prediction_df["prediction"]
df["confidence"] = prediction_df["confidence"]

print("Prediction columns added.")

print(
    df[
        [
            "customer_id",
            "risk_score",
            "prediction",
            "confidence"
        ]
    ].head()
)


scoring_date = datetime.today().strftime("%Y-%m-%d")

df["scoring_date"] = scoring_date

print("Scoring date:", scoring_date)

risk_table = df[
    [
        "customer_id",
        "risk_score",
        "prediction",
        "confidence",
        "scoring_date"
    ]
].copy()

print("Final risk table:")
print(risk_table.head())

print("\nShape:", risk_table.shape)


risk_table.to_sql(
    "customer_risk_table",
    engine,
    if_exists="replace",
    index=False
)

print(
    "customer_risk_table created successfully."
)

check_df = pd.read_sql(
    """
    SELECT *
    FROM customer_risk_table
    LIMIT 10
    """,
    engine
)

print(check_df)


prediction_counts = (
    risk_table["prediction"]
    .value_counts()
)

print("========== PREDICTION SUMMARY ==========")

print(prediction_counts)

prediction_percentages = (
    risk_table["prediction"]
    .value_counts(normalize=True)
    * 100
)

print("========== PREDICTION PERCENTAGE ==========")

print(
    prediction_percentages.round(2)
)


actual_churn_rate = (
    df["churn"]
    .mean()
    * 100
)

predicted_churn_rate = (
    (
        risk_table["prediction"]
        == "Likely to churn"
    ).mean()
    * 100
)

print("========== CHURN RATE COMPARISON ==========")

print(
    f"Actual churn rate: "
    f"{actual_churn_rate:.2f}%"
)

print(
    f"Predicted churn rate: "
    f"{predicted_churn_rate:.2f}%"
)





top_10_risk = risk_table.sort_values(
    by="risk_score",
    ascending=False
).head(10)

print("========== TOP 10 HIGHEST-RISK CUSTOMERS ==========")

print(
    top_10_risk.to_string(index=False)
)



sql6_df = pd.read_sql(
    """
    SELECT *
    FROM v_high_risk_customers
    """,
    engine
)

print("SQL6 high-risk count:", len(sql6_df))

print("\nSQL6 sample:")
print(sql6_df.head())




top_10_ids = set(
    top_10_risk["customer_id"]
)

sql6_ids = set(
    sql6_df["customer_id"]
)

overlap = top_10_ids.intersection(
    sql6_ids
)

print("========== SQL6 vs ML ==========")

print(
    "Top 10 ML high-risk customers:",
    len(top_10_ids)
)

print(
    "SQL6 rule-based high-risk customers:",
    len(sql6_ids)
)

print(
    "Customers appearing in both:",
    len(overlap)
)

print("\nOverlapping customers:")

print(sorted(overlap))




overlap_details = top_10_risk[
    top_10_risk["customer_id"].isin(overlap)
]

print(
    overlap_details.to_string(index=False)
)



print(
    f"""
========== INTERPRETATION ==========

The ML model identified the top 10 customers based on
predicted churn probability.

{len(overlap)} of these customers were also identified
by the SQL6 rule-based high-risk view.

Partial overlap is expected because SQL6 uses fixed
business rules, while the ML model considers learned
patterns across the engineered customer features.

Customers appearing in both lists are strong candidates
for proactive retention campaigns.
"""
)