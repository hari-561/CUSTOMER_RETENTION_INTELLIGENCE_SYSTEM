import pandas as pd
from staging import session, StagingCustomer

df = pd.read_csv("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/WA_Fn-UseC_-Telco-Customer-Churn.csv")
for _, row in df.iterrows():

    record = StagingCustomer(
        customerID=row["customerID"],
        gender=row["gender"],
        SeniorCitizen=row["SeniorCitizen"],
        Partner=row["Partner"],
        Dependents=row["Dependents"],
        tenure=row["tenure"],
        PhoneService=row["PhoneService"],
        MultipleLines=row["MultipleLines"],
        InternetService=row["InternetService"],
        OnlineSecurity=row["OnlineSecurity"],
        OnlineBackup=row["OnlineBackup"],
        DeviceProtection=row["DeviceProtection"],
        TechSupport=row["TechSupport"],
        StreamingTV=row["StreamingTV"],
        StreamingMovies=row["StreamingMovies"],
        Contract=row["Contract"],
        PaperlessBilling=row["PaperlessBilling"],
        PaymentMethod=row["PaymentMethod"],
        MonthlyCharges=row["MonthlyCharges"],
        TotalCharges=row["TotalCharges"],
        Churn=row["Churn"]
    )

    session.add(record)

session.commit()

