import os
import pandas as pd
import snowflake.connector
from row64tools import ramdb
from dotenv import load_dotenv


def Snowflake():
    
    # Please set the following environment variables: DBUser, DBPwd, DBAccount to proper values.
    load_dotenv("/home/row64/r64tools/db.env")
    
    print("----------- Connecting To Snowflake -----------")
    conn = snowflake.connector.connect(
        user=os.environ["DBUser"],
        password=os.environ["DBPwd"],
        account=os.environ["DBAccount"],
        database ="EXAMPLE"
    )

    print("----------- Connection Success! -----------")

    cur = conn.cursor().execute("SELECT * FROM SALES")
    df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
    
    df["SALES"] = pd.to_datetime(df["SALES"])

    print(df) # temporary - log the dataframe, remove for production use

    # more details on saving to .ramdb: https://pypi.org/project/row64tools/
    ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


Snowflake( )
