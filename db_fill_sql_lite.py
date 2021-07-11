from sqlalchemy import create_engine, Index, MetaData
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import sessionmaker
from train_data_status import TrainDataStatus, Base

import argparse
import pathlib
parser = argparse.ArgumentParser(description="Fills MySQL Database table with TrainData")
parser.add_argument("-p", "--port", dest="port", metavar="PORT", help="MySQL Instance Port", default=5588, type=int)
parser.add_argument("input_path", help="CSV file path", type=pathlib.Path)
args = parser.parse_args()

from dotenv import load_dotenv
import os
load_dotenv()
os.remove("tank.db")

engine = create_engine('sqlite:///tank.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import pandas as pd
print("Read CSV")
df = pd.read_csv(args.input_path)
print("Write to db")
df.to_sql("train_data_tmp", engine, if_exists='replace', dtype = {"station_uuid": VARCHAR(50)}, index=False, chunksize=500000)
print("Create index")
META_DATA = MetaData(bind=engine, reflect=True)
TRAIN_DATA_TABLE = META_DATA.tables['train_data_tmp']
uuid_index = Index("uuid_index", TRAIN_DATA_TABLE.c.station_uuid)
uuid_index.create(bind=engine)
session.execute("ALTER TABLE train_data_tmp RENAME TO train_data;")
status = TrainDataStatus(version=1, count=len(df))
session.add(status)
session.commit()
print("Finished")