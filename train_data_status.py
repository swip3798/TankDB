from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String
import datetime

Base = declarative_base()

class TrainDataStatus(Base):
    __tablename__ = "data_status"
    id = Column(Integer, primary_key = True, autoincrement = True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    version = Column(Integer)
    count = Column(Integer)
