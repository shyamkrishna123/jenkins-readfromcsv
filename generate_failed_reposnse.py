import pandas as pd
import datetime
import argparse
import requests
import json
import os
from pandas.core.frame import DataFrame

class ReadFromCSV:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
         
    def read_response_from_csv(self) -> DataFrame:
        col_list = ["URL", "responseCode", "responseMessage", "success", "failureMessage"]
        failed_results = pd.DataFrame([])
        results = pd.read_csv(self.input_file, usecols=col_list)
        return results
    
    def write_response_to_csv(self):
        results = self.read_response_from_csv()
        failed_results = results.loc[results["responseCode"] != 200]
        failed_results = failed_results.loc[results["responseCode"] != 201]
        if not os.path.isfile(self.output_file):
            failed_results.to_csv(self.output_file, mode='a', header=["responseCode", "responseMessage", "success", "failureMessage", "URL"])
        else:
            failed_results.to_csv(self.output_file, mode='a', header=False)
        
def get_argparser() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="Specify the file")
    arg_parser.add_argument("input_file", metavar="path", type=str, help="the path to file")
    arg_parser.add_argument("output_file", metavar="path", type=str, help="the path to file")
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    arg_parser = get_argparser()
    write_to_csv = ReadFromCSV(arg_parser.input_file,arg_parser.output_file)
    write_to_csv.write_response_to_csv()
