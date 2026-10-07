# import pandas as pd
# import numpy as np
# import logging

# logging.basicConfig(
# filename="data_cleaning.log",
# level=logging.INFO,
# format="%(asctime)s - %(levelname)s - %(message)s"
# )


# class customer_cleaner:
#     def __init__(self,df):
#         #self.df = pd.read_csv(path)
#         self.df = df
#         print(self.df.size)
#         logging.info("Customer Cleaner class created ...... ")
#         logging.info(f"Total number of Rows {self.df.shape[0]} ")
#         logging.info(f"Total number of Columns : {self.df.shape[1]}")
       

#     def standardize_column_names(self):
#         #print("before",self.df.columns)
#         logging.info("\n")
#         logging.info("Executing the standard column names....")
#         logging.info(f"Columns before standardizing : {self.df.columns}")

#         self.df.columns = (
#             self.df.columns
#             .str.replace(r'(?<!^)(?=[A-Z])', '_', regex=True)
#             .str.lower())
        
#         logging.info(f"Columns after standardizing : {self.df.columns}")

#     # def fix_total_charges(self):
#     #     logging.info("Executuing fix_total_charges..... ")
#     #     blank_count  = self.df["total_charges"].str.strip().eq("").sum()
#     #     logging.info(f"blankcount before  fixing : {blank_count}")
#     #     # self.df["total_charges"] = self.df["total_charges"].str.strip()
#     #     # self.df["total_charges"] = self.df["total_charges"].replace("",np.nan)
#     #     self.df["total_charges"] = self.df["total_charges"].replace(r"^\s*$",np.nan,regex=True)
#     #     blank_count  = self.df["total_charges"].str.strip().eq("").sum()
#     #     logging.info(f"blankcount after  fixing : {blank_count}")

#     #     self.df["total_charges"] = pd.to_numeric(self.df["total_charges"],errors="coerce")
#     #     logging.info("total_charges converted to numberic")



#     def fix_total_charges(self):


#         try:
#             logging.info("\n")
#             logging.info("Executing fix_total_charges...")

#             blank_count = self.df["total_charges"].str.strip().eq("").sum()
#             logging.info(f"Blank count before fixing: {blank_count}")

#             self.df["total_charges"] = self.df["total_charges"].replace(
#                 r"^\s*$",
#                 np.nan,
#                 regex=True
#             )

#             blank_count = self.df["total_charges"].fillna("").str.strip().eq("").sum()
#             logging.info(f"Blank count after fixing: {blank_count}")

#             self.df["total_charges"] = pd.to_numeric(
#                 self.df["total_charges"],
#                 errors="coerce"
#             )

#             logging.info("total_charges converted to numeric")
#         except KeyError:
#             logging.exception(" 'total_charges' column not found")
#         except AttributeError:
#             logging.exception("String operations failed. Check if DataFrame or column is valid.")
#         except Exception:
#             logging.exception("Unexpected error while fixing total_charges")
            

#     def normalize_binary_coumns(self):
#         logging.info("\n")

#         logging.info("Execitng Normalizing function ......")
     
#         logging.info(self.df[["partner","dependents","phone_service","paperless_billing","churn"]].head())
#         self.df["partner"] = self.df["partner"].map({"Yes":1,"No":0})
#         self.df["dependents"] = self.df["dependents"].map({"Yes":1,"No":0})
#         self.df["phone_service"] = self.df["phone_service"].map({"Yes":1,"No":0})
#         self.df["paperless_billing"] = self.df["paperless_billing"].map({"Yes":1,"No":0})
#         self.df["churn"] = self.df["churn"].map({"Yes":1,"No":0})
        
#         logging.info(f" after normalizing the vaues : {self.df[["partner","dependents","phone_service","paperless_billing","churn"]].head()}")

#     def handel_null(self):
#         logging.info("\n")
#         logging.info("Executting handel null values .........")
#         self.df["total_charges"] = self.df["total_charges"].fillna(self.df["monthly_charges"])
#         logging.info(f" null values after handling in total charges: {self.df["total_charges"].isna().sum()}")


#     def clean(self):
#         self.standardize_column_names()
#         self.fix_total_charges()
#         self.normalize_binary_coumns()
#         self.handel_null()

#         return self.df

#         # return self.df.to_csv("cleaned_data2.csv", index=False)



import pandas as pd
import numpy as np

class customer_cleaner:

    def __init__(self, df):
        self.df = df

        print("Customer Cleaner class created...")
        print(f"Total number of Rows: {self.df.shape[0]}")
        print(f"Total number of Columns: {self.df.shape[1]}")

    def standardize_column_names(self):

        print("\n")
        print("Executing standardize_column_names...")
        print(f"Columns before standardizing: {list(self.df.columns)}")

        self.df.columns = (
        self.df.columns
        .str.replace(
            r'(?<=[a-z0-9])(?=[A-Z])',
            '_',
            regex=True
        )
        .str.lower()
    )

        print(f"Columns after standardizing: {list(self.df.columns)}")

    def fix_total_charges(self):

        try:
            print("\n")
            print("Executing fix_total_charges...")

            blank_count = self.df["total_charges"].str.strip().eq("").sum()
            print(f"Blank count before fixing: {blank_count}")

            self.df["total_charges"] = self.df["total_charges"].replace(
                r"^\s*$",
                np.nan,
                regex=True
            )

            blank_count = (
                self.df["total_charges"]
                .fillna("")
                .str.strip()
                .eq("")
                .sum()
            )

            print(f"Blank count after fixing: {blank_count}")

            self.df["total_charges"] = pd.to_numeric(
                self.df["total_charges"],
                errors="coerce"
            )

            self.df["monthly_charges"] = pd.to_numeric(
                            self.df["monthly_charges"],
                            errors="coerce"
                        )
        

        except KeyError:
            print("ERROR: 'total_charges' column not found")

        except AttributeError:
            print("ERROR: String operations failed. Check DataFrame or column.")

        except Exception as e:
            print(f"ERROR: Unexpected error while fixing total_charges: {e}")

    def normalize_binary_columns(self):

        print("\n")
        print("Executing normalize_binary_columns...")

        print(
            self.df[
                [
                    "partner",
                    "dependents",
                    "phone_service",
                    "paperless_billing",
                    "churn"
                ]
            ].head()
        )

        self.df["partner"] = self.df["partner"].map({"Yes": 1, "No": 0})
        self.df["dependents"] = self.df["dependents"].map({"Yes": 1, "No": 0})
        self.df["phone_service"] = self.df["phone_service"].map({"Yes": 1, "No": 0})
        self.df["paperless_billing"] = self.df["paperless_billing"].map({"Yes": 1, "No": 0})
        self.df["churn"] = self.df["churn"].map({"Yes": 1, "No": 0})

        print(
            self.df[
                [
                    "partner",
                    "dependents",
                    "phone_service",
                    "paperless_billing",
                    "churn"
                ]
            ].head()
        )

       
    def handle_null(self):

        print("\n")
        print("Executing handle_null...")

        self.df["total_charges"] = self.df["total_charges"].fillna(
            self.df["monthly_charges"]
        )

        print(
            f"Null values after handling in total_charges: "
            f"{self.df['total_charges'].isna().sum()}"
        )

      

    def clean(self):

        self.standardize_column_names()
        self.fix_total_charges()
        self.normalize_binary_columns()
        self.handle_null()

        return self.df