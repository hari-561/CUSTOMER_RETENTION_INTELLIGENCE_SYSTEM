import pandas as pd

df = pd.read_csv("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/customer_churn.csv")

print("shape:")
print(df.shape)

print("columsn:")
print(df.columns)

print("dta types:")
print(df.dtypes)

print("null values:")
print(df.isnull().sum())

print("null percentage:")
print((df.isnull().sum() / len(df)) * 100)

# for col in df.columns:
#     print(f"\ncolumn:{col}")
#     print(df[col].value_counts(dropna=False))

# print(df.nunique()

for col in df.columns:
    unique_values = df[col].unique()
    print(col)
    print(f"unique values :{unique_values}")
    print("unique count:",len(unique_values))


churn_count = df["Churn"].value_counts()
print("churn count : ",churn_count)






print("TotalCharges:")
print(df["TotalCharges"].dtypes)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")
print(df["TotalCharges"].dtypes)
print(df["TotalCharges"].isnull().sum())

print(df[["tenure","MonthlyCharges","TotalCharges"]].describe())


print(df.index)

print(df.loc[1])


df.to_csv("cleaned_data1.csv", index=False)