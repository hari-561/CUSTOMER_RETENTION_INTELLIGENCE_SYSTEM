from cleanermodel import customer_cleaner
from pathlib import Path
from datetime import datetime
import pandas as pd
import logging
import time

logging.basicConfig(
    filename="data_cleaning_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_data(path):
    try:
        logging.info("Starting data loading...")
        df = pd.read_csv(path)
        logging.info(f"Data loaded successfully. Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        return df

    except Exception as e:
        logging.exception(f"Error while loading data: {e}")
        raise


def build_features(df):
    try:
        logging.info("Starting feature engineering...")

        df["high_charge_flag"] = df["monthly_charges"].apply(
            lambda x: 1 if x > df["monthly_charges"].median() else 0
        )
        # print(df["high_charge_flag"].head())

        cols = [
            "online_security",
            "online_backup",
            "device_protection",
            "tech_support",
            "streaming_t_v",
            "streaming_movies"
        ]

        df[cols] = df[cols].replace(
            {
                "Yes": 1,
                "No": 0,
                "No internet service": 0
            }
        )

        df["service_count"] = df[cols].sum(axis=1).astype(int)
        # print(df["service_count"].head())

        df["is_long_term_customer"] = df["tenure"].apply(
            lambda x: 1 if x >= 24 else 0
        )
        # print(df["is_long_term_customer"].head())

        df["has_streaming_bundle"] = (
            (df["streaming_t_v"] == 1)
            & (df["streaming_movies"] == 1)
        ).astype(int)
        # print(df["has_streaming_bundle"].head())

        df["auto_pay_flag"] = (
            df["payment_method"]
            .str.contains("automatic", case=False)
            .astype(int)
        )
        # print(df["auto_pay_flag"].head())

        new_features = [
            "high_charge_flag",
            "service_count",
            "is_long_term_customer",
            "has_streaming_bundle",
            "auto_pay_flag"
        ]

        corre = df[new_features].corrwith(df["churn"])
        # print(corre.sort_values(ascending=False))

        logging.info(
            f"Feature engineering completed successfully. Rows processed: {df.shape[0]}"
        )

        return df

    except Exception as e:
        logging.exception(f"Error during feature engineering: {e}")
        raise


def clean_data(df):
    try:
        logging.info("Starting data cleaning...")

        cleanobj = customer_cleaner(df)
        df = cleanobj.clean()

        logging.info(
            f"Data cleaning completed successfully. Rows after cleaning: {df.shape[0]}"
        )

        return df

    except Exception as e:
        logging.exception(f"Error during data cleaning: {e}")
        raise


def save_outputs(clean_df, feature_df, output_dir):
    try:
        logging.info("Saving output files...")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        clean_file = output_path / f"clean_data_{timestamp}.csv"
        feature_file = output_path / f"feature_data_{timestamp}.csv"

        clean_df.to_csv(clean_file, index=False)
        feature_df.to_csv(feature_file, index=False)

        logging.info(f"Clean data saved to: {clean_file}")
        logging.info(f"Feature data saved to: {feature_file}")

        # print(f"Clean data saved: {clean_file}")
        # print(f"Feature data saved: {feature_file}")

        return clean_file, feature_file

    except Exception as e:
        logging.exception(f"Error while saving output files: {e}")
        raise


if __name__ == "__main__":

    start_time = time.time()
    logging.info("=" * 60)
    logging.info("Customer Churn ETL Pipeline Started")

    try:
        df = load_data(
            "C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/WA_Fn-UseC_-Telco-Customer-Churn.csv"
        )

        df1 = clean_data(df)
        logging.info("Cleaning step completed.")

        df2 = build_features(df1)
        logging.info("Feature engineering step completed.")

        f1, f2 = save_outputs(df1, df2, "outputs")
        logging.info("Output saving step completed.")

        elapsed = time.time() - start_time

        logging.info("=" * 60)
        logging.info("Pipeline completed successfully.")
        logging.info(f"Total execution time: {elapsed:.2f} seconds")
        logging.info(f"Rows processed: {df2.shape[0]}")
        logging.info(f"Clean data file: {f1}")
        logging.info(f"Feature data file: {f2}")
        logging.info("=" * 60)

        # print(df2.head())

    except Exception as e:
        logging.exception("Pipeline execution failed.")
        raise