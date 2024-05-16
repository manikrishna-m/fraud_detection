import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import joblib

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.logger import get_logger
from src.exception import CustomException

# Restore the original sys.path
sys.path.pop()

# Get the logger
logger = get_logger()

@dataclass 
class DataPreprocessingPaths:
    df_path: str = "data/processed/input_data.csv"
    train_path: str = "data/processed/train_data.csv"
    test_path: str = "data/processed/test_data.csv"
    preprocessor_path: str = "data/processed/preprocessing.pkl"

class DataProcessing:
    def __init__(self):
        paths = DataPreprocessingPaths()
        self.df_path = paths.df_path
        self.train_path = paths.train_path
        self.test_path = paths.test_path
        self.preprocessing_path = paths.preprocessor_path

    def data_transformation(self):
        try:
            logger.info("Data transformation started")

            categorical_vars = ['type']
            numerical_vars = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']

            preprocessor_transformers = [
                ('num', Pipeline([
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', MinMaxScaler())
                ]), numerical_vars),
                ('cat', Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder())
                ]), categorical_vars),
            ]

            preprocessor = ColumnTransformer(preprocessor_transformers, remainder='drop')

            logger.info("Data transformation completed")

            return preprocessor

        except Exception as e:
            logger.exception("Data Transformation Exception: %s", e)
            raise CustomException(str(e))

    def data_preprocessing(self):
        try:
            df = pd.read_csv(self.df_path)
            logger.info("Reading data from saved folder completed")

            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['isFraud'])
            train_df.to_csv(self.train_path, index=False)
            test_df.to_csv(self.test_path, index=False)
            logger.info("Data splitting completed")

            logger.info("Obtaining preprocessing object")
            preprocessing_obj = self.data_transformation()

            logger.info("Applying label encoder on training and testing dataframes for target column")
            target_column = "isFraud"
            label_encoder = LabelEncoder()
            train_df[target_column] = label_encoder.fit_transform(train_df[target_column])
            test_df[target_column] = label_encoder.transform(test_df[target_column])

            input_feature_train_df = train_df.drop(columns=[target_column], axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column], axis=1)
            target_feature_test_df = test_df[target_column]

            logger.info("Applying preprocessing object on training and testing dataframes")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logger.info("Saving preprocessing object")
            os.makedirs(os.path.dirname(self.preprocessing_path), exist_ok=True)
            with open(self.preprocessing_path, "wb") as file_obj:
                joblib.dump(preprocessing_obj, file_obj)

            return input_feature_train_arr, target_feature_train_df, input_feature_test_arr, target_feature_test_df, self.preprocessing_path

        except Exception as e:
            logger.exception("Data Preprocessing Exception: %s", e)
            raise CustomException(str(e))

