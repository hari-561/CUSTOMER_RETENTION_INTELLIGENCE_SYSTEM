import os
import joblib
import pandas as pd


# --------------------------------------------------
# Load the trained model at module level
# --------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "tree_churn.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# These MUST match the columns used during training
# --------------------------------------------------

FEATURE_COLUMNS = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "high_charge_flag",
    "service_count",
    "is_long_term_customer",
    "has_streaming_bundle",
    "auto_pay_flag",
    "contract_Month-to-month",
    "contract_One year",
    "contract_Two year",
    "internet_service_DSL",
    "internet_service_Fiber optic",
    "internet_service_No"
]

# --------------------------------------------------
# Dataset average monthly charges
#
# Replace this with the actual average from your
# training dataset if you have it.
# --------------------------------------------------

DATASET_AVERAGE_MONTHLY_CHARGES = 64.76


# --------------------------------------------------
# 264. Preprocess one customer
# --------------------------------------------------

def preprocess_input(
    tenure,
    monthly_charges,
    contract_type,
    service_count,
    internet_service
):
    """
    Convert API input into a single-row DataFrame
    with exactly the same features used during training.
    """

    # Derived features
    total_charges = monthly_charges * tenure

    high_charge_flag = int(
        monthly_charges > DATASET_AVERAGE_MONTHLY_CHARGES
    )

    is_long_term_customer = int(
        tenure >= 24
    )

    # Default values for fields not collected by UI
    auto_pay_flag = 0
    has_streaming_bundle = 0

    # Start with all features as zero
    data = {
        column: 0
        for column in FEATURE_COLUMNS
    }

    # Numeric features
    data["tenure"] = tenure
    data["monthly_charges"] = monthly_charges
    data["total_charges"] = total_charges
    data["service_count"] = service_count

    data["high_charge_flag"] = high_charge_flag
    data["is_long_term_customer"] = is_long_term_customer
    data["auto_pay_flag"] = auto_pay_flag
    data["has_streaming_bundle"] = has_streaming_bundle

    if contract_type == "Month-to-month":
        data["contract_Month-to-month"] = 1

    elif contract_type == "One year":
        data["contract_One year"] = 1

    elif contract_type == "Two year":
        data["contract_Two year"] = 1

    else:
        raise ValueError(
            f"Invalid contract type: {contract_type}"
        )
    
    if internet_service == "DSL":
                data["internet_service_DSL"] = 1
        
    elif internet_service == "Fiber optic":
                data["internet_service_Fiber optic"] = 1
        
    elif internet_service == "No":
                data[" internet_service_No"] = 1
        
    else:
                raise ValueError(
                    f"Invalid internet service: {internet_service}"
                )
        

    # Create DataFrame
    input_df = pd.DataFrame(
    [data],
    columns=FEATURE_COLUMNS
)

    return input_df


# --------------------------------------------------
# 265. Predict churn
# --------------------------------------------------

def predict_churn(
    tenure,
    monthly_charges,
    contract_type,
    service_count,
    internet_service
):
    """
    Generate churn prediction and probability.
    """

    # Preprocess input
    input_df = preprocess_input(
        tenure=tenure,
        monthly_charges=monthly_charges,
        contract_type=contract_type,
        service_count=service_count,
        internet_service=internet_service

    )

    # Prediction
    prediction = model.predict(input_df)[0]

    # Probability of class 1 = churn
    probability = model.predict_proba(input_df)[0][1]

    # Confidence
    confidence = max(
        model.predict_proba(input_df)[0]
    )

    # Convert prediction to required text
    if prediction == 1:
        prediction_text = "Likely to churn"
    else:
        prediction_text = "Unlikely to churn"

    return {
        "risk_score": float(probability),
        "prediction": prediction_text,
        "confidence": float(confidence)
    }



