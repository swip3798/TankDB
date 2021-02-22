from dataprocessing import DataManager
import argparse
import pathlib

def generate_train_data(train_period = 7, daily_datapoints = 24, output_path = "TrainData.csv", output = print):
    output("Initialize history data...")
    dm = DataManager(train_period=train_period, daily_datapoints=daily_datapoints)
    output("Generate train data (can take some time)...")
    train_data = dm.generate_train_data()
    output("Save train data in csv file")
    train_data.to_csv(output_path, index=False)
    output("Finished!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates traindata based on the prices changes in the history data")
    parser.add_argument("-p", "--period", dest="train_period", metavar="P", help="Trainperiod in days", default=7, type=int)
    parser.add_argument("-d", "--daily-datapoints", dest="daily_datapoints", metavar="D", help="Number of daily train points (24 is one per hour)", default=24, type=int)
    parser.add_argument("output_path", help="Output file path, saved as csv file", type=pathlib.Path)
    args = parser.parse_args()
    generate_train_data(args.train_period, args.daily_datapoints, args.output_path)


