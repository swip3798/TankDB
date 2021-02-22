from sqlalchemy import create_engine, Index, MetaData
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql://root:passwort@127.0.0.1:5588/tankdb', echo=True)
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
session.execute("RENAME TABLE train_data_tmp TO train_data")
print("Finished")