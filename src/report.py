import io
import json
import numpy as np
import pandas as pd
from pathlib import Path
from tabulate2 import tabulate

class DataReport:
    def __init__(self, 
                 df: pd.DataFrame, 
                 report_path: str=(Path.cwd()/'report.txt').as_posix(), 
                 draft_path: str=(Path.cwd()/'draft_report.txt').as_posix(), 
                 meta_data_path: str=(Path.cwd()/'meta_data.json').as_posix()) -> None:

        self.df = df
        self.report_path = report_path
        self.draft_path = draft_path
        self.meta_data_path = meta_data_path

# TODO: add meta data from this function to a json file
    def perform_basic_cleaning(self):
        meta_data = {}
        self.df.columns = [column.strip().lower() for column in self.df.columns.tolist()]

        # string pre-processing
        cat_cols = self.df.select_dtypes("object").columns.tolist()
        self.df[cat_cols] = self.df[cat_cols].astype(str).map(lambda x: x.strip().lower())
        meta_data['string_preprocessing'] = True

        # duplications
        meta_data['duplications'] = self.df.duplicated().sum(axis=0)
        self.df.drop_duplicates(inplace=True)

        # detection of single-value columns
        single_value_columns = self.df\
                .value_counts().to_frame('uniq_values')\
                .query('uniq_values == 1', inplace=True).index.tolist()
        meta_data['single_values_columns'] = single_value_columns

        try: 
            self.df.drop(single_value_columns, axis=1, inplace=True) 
        except Exception as e: 
            print (f"Error: {e}")

        json.dump(self.meta_data_path)

        return self

    def summarize_general_info(self, 
                               append_to_report: bool = False) -> None:
        # dataframe info
        buffer = io.StringIO()
        self.df.info(buf=buffer)

        info = f"Shape: {self.df.shape}\
                \nInfo: \n{buffer.getvalue()}"

        if append_to_report:
            with open(self.report_file_path, 'w+') as f:
                print(info, file=f)
        else:
            with open(self.draft_file_path, 'w') as f:
                print(info, file=f)

    def summarize_statistics(self, 
                             append_to_report: bool = False) -> None:
        pass

    def append_to_report(self, 
                         info: str) -> None:
        with open(self.report_file_path, 'w+') as f:
            print(info, file=f)

    def export(self) -> None:
        pass
