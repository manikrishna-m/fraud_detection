import pandas as pd
import sys
import joblib
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.exception import CustomException
from src.logger import get_logger
from src.data_components.data_injection_scripts import DataInjection
from src.data_components.data_preprocessing_scripts import DataProcessing
from src.data_components.model_evaluation_scripts import ModelTrainer

# Restore the original sys.path
sys.path.pop()

# Get the logger
logger = get_logger()


class PredictPipeline:
    def __init__(self):
        self.processor_path = 'data/processed/preprocessing.pkl'
        self.model_path = 'data/processed/model.pkl'

    def predict(self, data):
        try:
            with open(self.processor_path, "rb") as file_obj:
                processor = joblib.load(file_obj)

            with open(self.model_path, "rb") as file_obj:
                model = joblib.load(file_obj)

            return model.predict(processor.transform(data))
        
        except Exception as e:
            logger.exception("Prediction Exception: %s", e)
            raise CustomException(e, sys)


class CustomData:
    def __init__(self, step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, trans_type):
        self.step = step
        self.trans_type = trans_type
        self.amount = amount
        self.oldbalanceOrg = oldbalanceOrg
        self.newbalanceOrig = newbalanceOrig
        self.oldbalanceDest = oldbalanceDest
        self.newbalanceDest = newbalanceDest


    def to_dataframe(self):
        try:
            data_dict = {
                'step': [self.step],
                'type': [self.trans_type],
                'amount': [self.amount],
                'oldbalanceOrg': [self.oldbalanceOrg],
                'newbalanceOrig': [self.newbalanceOrig],
                'oldbalanceDest': [self.oldbalanceDest],
                'newbalanceDest': [self.newbalanceDest],
            }

            return pd.DataFrame.from_dict(data_dict, orient='columns')

        except Exception as e:
            logger.exception("Data Conversion Exception: %s", e)
            raise CustomException(e, sys)
