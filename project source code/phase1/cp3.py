from cleanermodel import customer_cleaner
import pandas as pd

df = pd.read_csv("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/phase1/cleaned_data2.csv")
print(df.columns)

print(" churn rate by contract type :")
chrunrate_contract = df.groupby("contract")["churn"].mean().mul(100).sort_values(ascending=False)
print(chrunrate_contract)
print("highest churn values: ", chrunrate_contract.iloc[0])

chrunrate_internet_service = df.groupby("internet_service")["churn"].mean().mul(100).sort_values(ascending=False)
print(chrunrate_internet_service)

print(" churn rate by contract type :")
chrunrate_payment_method = df.groupby("payment_method")["churn"].mean().mul(100).sort_values(ascending=False)
print(chrunrate_payment_method)

df["tenure_bucket"] = pd.cut(
    df["tenure"],
    bins=[0, 12, 24, 48, 72],
    labels=["0-12", "13-24", "25-48", "49-72"],
    include_lowest=True
)

print(df[["tenure", "tenure_bucket"]].head())

print(" churn rate by tenure_bucket :")
chrunrate_tenure_bucket = df.groupby("tenure_bucket")["churn"].mean().mul(100).sort_values(ascending=False)
print(chrunrate_tenure_bucket)

avg_monthly_charges = (
    df.groupby("churn")["monthly_charges"]
      .mean()
)

print(avg_monthly_charges)

print(df["monthly_charges"].head())


churn_rate_combo = (
    df.groupby(["contract", "internet_service"])["churn"]
      .mean()
      .mul(100)
      .sort_values(ascending=False)
)

print(churn_rate_combo)



df.to_csv("cleaned_data3.csv",index = False)
print("cp3 completed......")



