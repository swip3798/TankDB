import pandas as pd
from utils import pad

def read_prices(day, month, year):
    return pd.read_csv ('tankerkoenig-data/prices/' + str(year) + '/' + pad(month) + '/' + str(year) + '-' + pad(month) + '-' + pad(day) + '-prices.csv')
    
def read_stations(day, month, year):
    return pd.read_csv ('tankerkoenig-data/stations/' + str(year) + '/' + pad(month) + '/' + str(year) + '-' + pad(month) + '-' + pad(day) + '-stations.csv')

def get_prices_by_date(date_obj):
    return read_prices(date_obj.day, date_obj.month, date_obj.year)

def get_stations_by_date(date_obj):
    return read_stations(date_obj.day, date_obj.month, date_obj.year)