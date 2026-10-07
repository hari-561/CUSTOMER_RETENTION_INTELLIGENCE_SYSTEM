import pandas as pd


df = pd.read_csv("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/phase1/cleaned_data3.csv")

df["high_charge_flag"] = df["monthly_charges"].apply(lambda x : 1 if x > df["monthly_charges"].median() else 0 )
print(df["high_charge_flag"].head())


cols = ["online_security", "online_backup", "device_protection", "tech_support", "streaming_t_v", 
"streaming_movies" ]



df[cols] = df[cols].replace({"Yes": 1, "No": 0, "No internet service":0})

df["service_count"] = df[cols].sum(axis=1).astype("int")
print(df["service_count"].head())

df["is_long_term_customer"] = df["tenure"].apply(lambda x: 1 if x >= 24 else 0)
print(df["is_long_term_customer"].head())

df["has_streaming_bundle"] = ((df["streaming_t_v"] == 1) & (df["streaming_movies"]==1)).astype(int)
print(df["has_streaming_bundle"].head())

#df["auto_pay_flag"] = df["payment_method"].apply(lambda x: 1 if x=="automatic" else 0)
df["auto_pay_flag"] = df["payment_method"].str.contains("automatic",case = False).astype(int)
print(df["auto_pay_flag"].head())

new_features = [
    "high_charge_flag",
    "service_count",
    "is_long_term_customer",
    "has_streaming_bundle",
    "auto_pay_flag"
]
corre = df[new_features].corrwith(df["churn"])
print(corre.sort_values(ascending=False))

df.to_csv("cleaned_data4.csv",index = False)