import pandas as pd
import glob
import os
from core.config.paths import output_path


class FilesCombiner:
    def __init__(self):
        self.csv_file_list = glob.glob(os.path.join(output_path, "*.csv"))

    def combiner(self):
        combined_csv = pd.concat(
            [
                pd.read_csv(each_csv, low_memory=False)
                for each_csv in self.csv_file_list
            ],
            sort=False,
        ).fillna("")
        combined_csv.drop_duplicates(inplace=True, keep="last")
        combined_csv.to_csv(os.path.join(output_path, "combined_csv.csv"), index=False)

    def start(self):
        print("Combining files together.")
        try:
            self.combiner()
        except ValueError:
            print("No Data in API")
