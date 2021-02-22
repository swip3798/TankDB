from enum import Enum
import pandas as pd
from datetime import date, datetime, timedelta, timezone
from .csv_import import get_stations_by_date, get_prices_by_date
import mpu
import tqdm

class FuelType(Enum):
    E5 = "e5"
    E10 = "e10"
    DIESEL = "diesel"

class DataManager():
    def __init__(self, auto_init = True, train_period = 28, daily_datapoints = 24):
        self.train_period = train_period
        self.daily_datapoints = daily_datapoints
        if auto_init:
            self.init_data()
    
    def init_data(self):
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        self.data_days = [self.yesterday - timedelta(days=1)*i for i in range(self.train_period + 1)]
        self.train_days = self.data_days[:-1]
        self.dp_delta = timedelta(days=1) / self.daily_datapoints
        self.train_dps = []
        for train_day in self.train_days:
            start = datetime.combine(train_day, datetime.min.time(), timezone.utc)
            self.train_dps += [start + self.dp_delta*i for i in range(self.daily_datapoints)]
        self.train_dps.sort()
        self.df_stations = get_stations_by_date(self.yesterday)
        self.df_prices = pd.concat([get_prices_by_date(day) for day in self.data_days])
        self.df_prices['date'] = pd.to_datetime(self.df_prices['date'], utc = True)
        self.df_prices = self.df_prices.merge(self.df_stations[['uuid', 'latitude', 'longitude']], left_on='station_uuid', right_on='uuid').sort_values(by='date', ascending=True)
        del self.df_prices['uuid']
    
    def filter_prices_by_station(self, station_id):
        return self.df_prices[self.df_prices.station_uuid==station_id]
    
    def filter_prices_by_stations(self, station_ids):
        return self.df_prices[self.df_prices.station_uuid.isin(station_ids)]
    
    def get_station_data(self, station_id):
        return self.df_stations[self.df_stations.uuid==station_id].to_dict('records')[0]

    def get_stations_data(self, station_ids):
        return self.df_stations[self.df_stations.uuid.isin(station_ids)].to_dict('records')
    
    def get_k_nearest_stations(self, station_data, k = 5):
        distances = self.df_stations.apply(lambda row: mpu.haversine_distance([station_data["latitude"], station_data["longitude"]], [row["latitude"], row["longitude"]]), axis = 1)
        distances.name = "distances"
        dfsd = pd.concat([self.df_stations, distances], axis=1)
        return dfsd.sort_values(by='distances').head(k+1).tail(k)
    
    def generate_train_data(self):
        dp_index = 0
        hour_prices = {}
        new_dp = False
        dp = self.train_dps[0]
        df_chunks = []
        for _, row in tqdm.tqdm(self.df_prices.iterrows(), total=len(self.df_prices)):
            try:
                while row['date'] > (self.train_dps[dp_index]):
                    dp_index += 1
                    new_dp = True
            except IndexError:
                break
            if new_dp:
                new_dp = False
                dp = self.train_dps[dp_index]
                df_chunks.append(pd.DataFrame(list(hour_prices.values())))
                for uuid in hour_prices:
                    hour_prices[uuid] = {
                        "lat": hour_prices[uuid]["lat"],
                        "lng": hour_prices[uuid]["lng"],
                        "station_uuid": hour_prices[uuid]["station_uuid"],
                        "hour": dp.hour,
                        "dom": dp.day,
                        "month": dp.month,
                        "year": dp.year,
                        "dow": dp.weekday(),
                        "e5": hour_prices[uuid]["e5"],
                        "e10": hour_prices[uuid]["e10"],
                        "diesel": hour_prices[uuid]["diesel"],
                    }
            hour_prices[row['station_uuid']] = {
                        "lat": row["latitude"],
                        "lng": row["longitude"],
                        "station_uuid": row["station_uuid"],
                        "hour": dp.hour,
                        "dom": dp.day,
                        "month": dp.month,
                        "year": dp.year,
                        "dow": dp.weekday(),
                        "e5": row["e5"],
                        "e10": row["e10"],
                        "diesel": row["diesel"],
                    }
        return pd.concat(df_chunks)
        # return df_train_data.to_csv("TrainData.csv", index=False)