from sqlalchemy import text
from fastapi import HTTPException


def get_churn_summary(db):
    # Overall churn summary
    overall_query = text("""
        SELECT
            COUNT(*) AS total_customers,
            SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) AS total_churned,
            CAST(SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) AS FLOAT)
                / NULLIF(COUNT(*), 0) AS churn_rate
        FROM fact_customer_account
    """)

    overall_result = db.execute(overall_query).mappings().first()

    # Churn rate by contract type
    contract_query = text("""
        SELECT
            dc.contract_name AS contract_type,
            CAST(SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) AS FLOAT)
                / NULLIF(COUNT(*), 0) AS churn_rate
        FROM fact_customer_account
        JOIN dim_contract dc ON fact_customer_account.contract_key = dc.contract_key
        GROUP BY dc.contract_name
        ORDER BY dc.contract_name
    """)

    contract_results = db.execute(contract_query).mappings().all()

    # Churn rate by internet service
    internet_query = text("""
        SELECT
            scr.internet_service,
            CAST(SUM(CASE WHEN scr.churn = 1 THEN 1 ELSE 0 END) AS FLOAT)
                / NULLIF(COUNT(*), 0) AS churn_rate
        FROM fact_customer_account
        JOIN stg_customer_raw scr ON fact_customer_account.customer_id = scr.customer_id
        GROUP BY scr.internet_service
        ORDER BY scr.internet_service
    """)

    internet_results = db.execute(internet_query).mappings().all()

    return {
        "summary": {
            "total_customers": overall_result["total_customers"],
            "total_churned": overall_result["total_churned"],
            "churn_rate": float(overall_result["churn_rate"] or 0)
        },
        "churn_by_contract_type": [
            {
                "contract_type": row["contract_type"],
                "churn_rate": float(row["churn_rate"] or 0)
            }
            for row in contract_results
        ],
        "churn_by_internet_service": [
            {
                "internet_service": row["internet_service"],
                "churn_rate": float(row["churn_rate"] or 0)
            }
            for row in internet_results
        ]
    }






def get_high_risk_customers(
    db,
    limit: int = 50,
    min_tenure: int | None = None,
    max_tenure: int | None = None
):
    query = """
        SELECT
            customer_id,
            tenure,
            monthly_charges,
            contract_type,
            risk_reason
        FROM v_high_risk_customers
        WHERE 1=1
    """

    params = {}

    if min_tenure is not None:
        query += " AND tenure >= :min_tenure"
        params["min_tenure"] = min_tenure

    if max_tenure is not None:
        query += " AND tenure <= :max_tenure"
        params["max_tenure"] = max_tenure

    query += " LIMIT :limit"
    params["limit"] = limit

    results = (
        db.execute(text(query), params)
        .mappings()
        .all()
    )
    print(query)
    print(params)

    return [dict(row) for row in results]





def get_customer_features(db, customer_id: str):
    query = text("""
        SELECT
            customer_id,
            services_count,
            high_charge_flag,
            is_long_term_contract,
            auto_pay_flag,
            monthly_charges,
            total_charges
        FROM customer_ml_features
        WHERE customer_id = :customer_id
    """)

    result = (
        db.execute(query, {"customer_id": customer_id})
        .mappings()
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' not found"
        )

    return dict(result)

