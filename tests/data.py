import sys
from pathlib import Path
sys.path.append((Path.cwd()/'src').as_posix())
from _data import DataAnalyzer

paths = {
        'csv': (Path.cwd()/'resource'/'data'/'raw'/'general.csv').as_posix(), 
        'des': (Path.cwd()/'resource'/'data'/'cleaned'/'general.csv').as_posix(), 
        'report': (Path.cwd()/'resource'/'report'/'report.txt').as_posix(), 
        'draft': (Path.cwd()/'resource'/'report'/'draft.txt').as_posix(), 
}

# FSBA: for sale by owner
# reasons to leave out some columns: dominance of missing values, out of scope 
kept_cols =  ['zipcode', 'city', 'state', 'latitude', 'longitude',
              'bathrooms', 'bedrooms', 'livingArea', 'homeType',
              'isPremierBuilder', 'currency', 'country', 'taxAssessedValue', 
              'lotAreaValue', 'lotAreaUnit', 'price'
]

data_analyzer = DataAnalyzer(paths, kept_cols)
data_analyzer\
        .preprocess()\
        .get_descriptive_stats()
