import sqlite3
import time
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData
import pandas as pd
engine = create_engine('sqlite:///tank.db', echo=False)
meta = MetaData(bind=engine, reflect=True)
traindata_table = meta.tables["train_data"]
start = time.time()
station_uuids = ["9f6c0314-c88d-4184-9a71-06b61208fda3","00062379-5286-4444-8888-acdc00062379","0360ce43-06c6-4c8f-b141-35461117e016"]
s = select([traindata_table]).where(traindata_table.c.station_uuid.in_(station_uuids))
df = pd.read_sql_query(
    s,
    engine
)
print("Time:", time.time() - start)
print(df)
con = sqlite3.connect("tank.db")
start = time.time()
res = con.execute("""SELECT * FROM train_data WHERE station_uuid in (?,?,?) """, station_uuids).fetchall()
df2 = pd.DataFrame(res, columns=["lat","lng","station_uuid","hour","dom","month","year","dow","e5","e10","diesel"])
print("Time:", time.time() - start)
print(df2)
print(df.dtypes)
print(df2.dtypes)