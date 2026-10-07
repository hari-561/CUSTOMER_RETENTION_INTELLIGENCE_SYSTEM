import pandas as pd
import numpy as np
import logging
from cleanermodel import customer_cleaner

logging.basicConfig(
filename="data_cleaning.log",
level=logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s"
)


cls = customer_cleaner("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/WA_Fn-UseC_-Telco-Customer-Churn.csv")
cls.clean()