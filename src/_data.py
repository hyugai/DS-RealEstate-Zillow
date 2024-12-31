import json
import numpy as np
import pandas as pd
from typing import Self
from io import StringIO
from tabulate2 import tabulate
from scipy.stats import chi2_contingency

class ReportWriter:
    def __init__(self, 
                 paths: dict[str, str]) -> None:
        self.paths = paths

    def __convert(self, 
                content: dict[str, str]) -> list[str]:
        lines = [title + '\n' + data for title, data in content.items()] # re-add the new line character '\n'

        return lines

    def write_draft(self, 
                    info: dict[str, str]):
        with open(self.paths['draft'], 'w') as f:
                f.writelines(self.__convert(info))

    def write_report(self,
                      info: dict[str, str], 
                      is_overwritten: bool) -> None: 
        content = {}
        with open(self.paths['report'], 'r') as f:
            lines = f.readlines()
            current_title: str

            for line in lines:
                if line.startswith('##'):
                    current_title = line.strip() # remove the new line character '\n' created when reading the file above
                    content[current_title] = ''
                else:
                    content[current_title] += line

        for title, data in info.items():
            if is_overwritten:
                content[title] = data
            else:
                content[title] += data

        with open(self.paths['report'], 'w') as f:
            f.writelines(self.__convert(content))

class DataAnalyzer(ReportWriter):
    def __init__(self,
                 paths: dict[str, str], 
                 kept_cols: list[str]) -> None:
        super().__init__(paths)
        self.kept_cols = kept_cols

        self.df_cleaned: pd.DataFrame

    def __find_value_above_threshold(self, 
                                     square_mat: np.ndarray,
                                     threshold: int, 
                                     cols: list[str]) -> list[str]:
        results = []
        num_iters = len(cols)
        i = 1
        while i <= num_iters:
            for j in range(i):
                if square_mat[i, j] >= threshold:
                    results.append(square_mat[i, j])

        return results

    def preprocess(self, 
                   is_exported: bool=False) -> Self:
        # load info as json
        raw_json = pd.read_csv(self.paths['csv'])\
                    .map(lambda x: json.loads(x)['homeInfo'])\
                    .values.ravel()
        df_base = pd.json_normalize(raw_json)

        # remove duplications
        counts = df_base.duplicated(subset='zpid').sum()
        if counts != 0:
            df_base.drop_duplicates(subset='zpid')

        # remove irrelevant columns 
        df_base.columns = [c.strip() for c in df_base.columns.tolist()]

        if self.kept_cols:
            cols_to_remove = [c for c in df_base.columns.tolist() if c not in self.kept_cols]
            df_base.drop(cols_to_remove, axis=1, inplace=True)

        # reindex columns
        df_base = df_base.reindex(labels=self.kept_cols, axis=1)

        #  remove single-value columns
        single_value_cols = df_base\
                .nunique()\
                .to_frame('nuniq').query("nuniq == 1").index.tolist()
        if single_value_cols:
            df_base.drop(single_value_cols, axis=1, inplace=True)

        # convert "CAD" to "USD"
        df_base[['price', 'taxAssessedValue']] = np.where(df_base['currency'].to_frame('currency') == 'CAD', 
                                                             df_base[['price', 'taxAssessedValue']] * 0.7, df_base[['price', 'taxAssessedValue']])
        df_base.drop('currency', axis=1, inplace=True)

        # convert "arces" to "sqft"
        df_base['lotAreaValue'] = np.where(df_base['lotAreaUnit'] == 'sqft', 
                                           df_base['lotAreaValue'].div(43560), df_base['lotAreaValue'])
        df_base.drop('lotAreaUnit', axis=1, inplace=True)

        # convert "bool" into "str"
        bool_cols = df_base.select_dtypes(bool).columns.tolist()
        df_base[bool_cols] = df_base[bool_cols].astype(str)

        # report
        buf = StringIO()
        df_base.info(buf=buf)
        self.write_report({'##Info': '\n' + buf.getvalue() + '\n'}, True)

        # export
        if is_exported:
            df_base.to_csv(self.paths['export'], index=False)

        self.df_cleaned = df_base

        return self

    def get_descriptive_stats(self,
                          is_attached_to_report: bool=False) -> Self:
        df = self.df_cleaned.copy()

        # report
        cat_stats = '\n' + tabulate(df.select_dtypes(include="object").describe().T, headers="keys", tablefmt="psql") + '\n'
        num_stats = '\n' + tabulate(df.select_dtypes(include=np.number).describe([0.01, 0.25, 0.50, 0.75, 0.99]).T, headers="keys", tablefmt="psql") + '\n'
        self.write_report({'##Categorical Stats': cat_stats, '##Numeric Stats': num_stats}, True)

        return self

    def get_inferential_stats(self,
                              is_attached_to_report: bool=False) -> Self:
        df = self.df_cleaned.copy()
        cat_cols = df.select_dtypes('object').columns.tolist()
        num_cols = df.select_dtypes(np.number).columns.tolist()

        # cat: dependency test
        num_iters = len(cat_cols)
        arr = np.zeros((num_iters, num_iters))

    def analyze_price(self) -> None:
        pass
