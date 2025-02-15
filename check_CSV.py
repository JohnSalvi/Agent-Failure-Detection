import pandas as pd

df = pd.read_csv("processed_success.csv")
print("Columns in processed_success.csv:", df.columns)

df_fail = pd.read_csv("processed_failure.csv")
print("Columns in processed_failure.csv:", df_fail.columns)