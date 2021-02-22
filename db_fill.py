from sqlalchemy import create_engine, Index, MetaData
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import sessionmaker
from train_data_status import TrainDataStatus, Base

from dotenv import load_dotenv
import os
load_dotenv()
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

engine = create_engine('mysql://root:{}@127.0.0.1:5588/tankdb'.format(DB_PASSWORD), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import pandas as pd
print("Read CSV")
df = pd.read_csv("TrainData.csv")
print("Write to db")
df.to_sql("train_data_tmp", engine, if_exists='replace', dtype = {"station_uuid": VARCHAR(50)}, index=False, chunksize=500000)
print("Create index")
META_DATA = MetaData(bind=engine, reflect=True)
TRAIN_DATA_TABLE = META_DATA.tables['train_data_tmp']
uuid_index = Index("uuid_index", TRAIN_DATA_TABLE.c.station_uuid)
uuid_index.create(bind=engine)
try:
    session.execute("RENAME TABLE train_data TO train_data_old, train_data_tmp TO train_data")
    session.execute("DROP TABLE train_data_old")
except:
    session.execute("RENAME TABLE train_data_tmp TO train_data")
status = TrainDataStatus(version=1, count=len(df))
session.add(status)
session.commit()
print("Finished")