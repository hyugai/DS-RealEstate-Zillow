import json
import pandas as pd

import sys
from pathlib import Path
sys.path.append((Path.cwd()/'src').as_posix())
from report import DataReport

# TODO: drop features having only one unique value
raw_csv_path = (Path.cwd()/'resource'/'data'/'raw'/'general_info_json.csv').as_posix()
general_info_json = pd.read_csv(raw_csv_path)\
        .map(lambda x: json.loads(x)['homeInfo'])\
        .values.ravel()
df_raw = pd.json_normalize(general_info_json)

# 
report_file_path = (Path.cwd()/'life_cycle'/'data_understanding'/'report.txt').as_posix()
draft_file_path = (Path.cwd()/'life_cycle'/'data_understanding'/'draft.txt').as_posix()
report = DataReport(df_raw, report_file_path, draft_file_path)
report\
        .perform_basic_cleaning()\
        .summarize_general_info(append_to_report=False)
