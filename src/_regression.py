from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split, RepeatedKFold
from sklearn.metrics import root_mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor 
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor

def load_models() -> list[tuple]:
    models = []
    models.append(('LR', LinearRegression(n_jobs=-1)))
    models.append(('SVM', SVR()))
    models.append(('KNN', KNeighborsRegressor(n_jobs=-1)))
    models.append(('CART', DecisionTreeRegressor()))
    models.append(('ET', ExtraTreesRegressor()))
    models.append(('RF', RandomForestRegressor(n_jobs=-1)))
    models.append(('GB', GradientBoostingRegressor()))

    return models 

def prepare_data_for_regression():
    pass
