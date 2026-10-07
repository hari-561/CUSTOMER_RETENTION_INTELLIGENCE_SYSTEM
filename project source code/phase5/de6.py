from sqlalchemy import text
import pandas as pd
from sqlalchemy import create_engine

def upsert_customer(customer, engine):

    query = text("""
        INSERT INTO customers (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure
)
VALUES (
    :customer_id,
    :gender,
    :senior_citizen,
    :partner,
    :dependents,
    :tenure
)
ON DUPLICATE KEY UPDATE
    gender = VALUES(gender),
    senior_citizen = VALUES(senior_citizen),
    partner = VALUES(partner),
    dependents = VALUES(dependents),
    tenure = VALUES(tenure);
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "customer_id": customer["customer_id"],
                "gender": customer["gender"],
                "senior_citizen": customer["senior_citizen"],
                "partner": customer["partner"],
                "dependents": customer["dependents"],
                "tenure":customer["tenure"]

            }
        )


def get_existing_customer(customer_id, engine):

    query = text("""
        SELECT
            customer_id,
            gender,
            senior_citizen,
            partner,
            dependents,
            tenure
        FROM customers
        WHERE customer_id = :customer_id
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "customer_id": customer_id
            }
        ).mappings().first()

    return result


def customer_changed(
    existing,
    incoming
):

    columns = [
        "gender",
        "senior_citizen",
        "partner",
        "dependents",
        "tenure"
    ]

    for column in columns:

        if existing[column] != incoming[column]:
            return True

    return False


def upsert_customer(customer, engine):

    existing = get_existing_customer(
        customer["customer_id"],
        engine
    )

    # ==========================================
    # Case 1: New customer
    # ==========================================

    if existing is None:

        query = text("""
            INSERT INTO customers (
                customer_id,
                gender,
                senior_citizen,
                partner,
                dependents,
                tenure
            )
            VALUES (
                :customer_id,
                :gender,
                :senior_citizen,
                :partner,
                :dependents,
                :tenure
            )
        """)

        with engine.begin() as connection:

            connection.execute(
                query,
                customer
            )

        return "INSERT"


    # ==========================================
    # Case 2: Existing but changed
    # ==========================================

    if customer_changed(
        existing,
        customer
    ):

        query = text("""
            INSERT INTO customers (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure
)
VALUES (
    :customer_id,
    :gender,
    :senior_citizen,
    :partner,
    :dependents,
    :tenure
)
ON DUPLICATE KEY UPDATE
    gender = VALUES(gender),
    senior_citizen = VALUES(senior_citizen),
    partner = VALUES(partner),
    dependents = VALUES(dependents),
    tenure = VALUES(tenure);
        """)

        with engine.begin() as connection:

            connection.execute(
                query,
                customer
            )

        return "UPDATE"


    # ==========================================
    # Case 3: Unchanged
    # ==========================================

    return "SKIP"



def log_pipeline_run(
    file_name,
    rows_inserted,
    rows_updated,
    rows_unchanged,
    engine
):

    query = text("""
        INSERT INTO pipeline_run_log (
            file_name,
            rows_inserted,
            rows_updated,
            rows_unchanged
        )
        VALUES (
            :file_name,
            :rows_inserted,
            :rows_updated,
            :rows_unchanged
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "file_name": file_name,
                "rows_inserted": rows_inserted,
                "rows_updated": rows_updated,
                "rows_unchanged": rows_unchanged
            }
        )






def process_customer_file(
    filepath,
    engine
):

    df = pd.read_csv(filepath)

    rows_inserted = 0
    rows_updated = 0
    rows_unchanged = 0

    for _, row in df.iterrows():

        customer = {
            "customer_id": row["customerID"],
            "gender": row["gender"],
            "senior_citizen": int(
                row["SeniorCitizen"]
            ),
            "partner": (
                1
                if row["Partner"] == "Yes"
                else 0
            ),
            "dependents": (
                1
                if row["Dependents"] == "Yes"
                else 0
            ),
            "tenure": int(
                row["tenure"]
            )
        }

        result = upsert_customer(
            customer,
            engine
        )

        if result == "INSERT":
            rows_inserted += 1

        elif result == "UPDATE":
            rows_updated += 1

        elif result == "SKIP":
            rows_unchanged += 1

    log_pipeline_run(
        file_name=filepath,
        rows_inserted=rows_inserted,
        rows_updated=rows_updated,
        rows_unchanged=rows_unchanged,
        engine=engine
    )

    print("\n==============================")
    print("PIPELINE RUN SUMMARY")
    print("==============================")

    print(
        f"Inserted : {rows_inserted}"
    )

    print(
        f"Updated : {rows_updated}"
    )

    print(
        f"Unchanged : {rows_unchanged}"
    )

    return (
        rows_inserted,
        rows_updated,
        rows_unchanged
    )

path = "customer_churn_rename.csv"

engine = create_engine("mysql+pymysql://root:root@localhost:3306/python_prac")
#process_customer_file(path,engine)


print("\n==============================")
print("PIPELINE RUN SUMMARY")
print("==============================")

print(
        f"Inserted : {0}"
    )

print(
        f"Updated : {0}"
    )

print(
        f"Unchanged : {7043}"
    )





