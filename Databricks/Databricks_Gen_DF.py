import pandas as pd
from row64tools import ramdb

data = {
"Date": ["2025-01-21 13:23:44","2025-01-21 13:23:52"],
"Amount": [446.57, 287.24],
"Product": ["Seal SE Robotic Pool Vacuum", "Tikom Robot Vacuum and Mop"],
}
df = pd.DataFrame(data)

df["Date"] = pd.to_datetime(df["Date"])
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

print(df)
rdbPath = os.getcwd() + "test.ramdb"
ramdb.save_from_df(df, rdbPath)



