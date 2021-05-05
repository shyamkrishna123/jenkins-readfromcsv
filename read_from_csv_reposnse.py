import csv
import argparse

class ReadCsv:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
def get_argparser() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="Specify the file")
    arg_parser.add_argument("file_path", metavar="path", type=str, help="the path to file")
    args = arg_parser.parse_args()
    return args

with open()
