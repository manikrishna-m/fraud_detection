import sys
import pandas as pd
from dataclasses import dataclass
from pathlib import Path

# Modify sys.path to include the parent directory for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.logger import get_logger
from src.exception import CustomException
# Restore the original sys.path
sys.path.pop()

# Get the logger
logger = get_logger()

@dataclass
class DataInjectionPaths:
    input_data_path: str = "data/input/input_data.csv"
    train_test_data_path: str = "data/processed/input_data.csv"

class DataInjection:
    def __init__(self):
        data_inj_path_obj = DataInjectionPaths()
        self.input_path = data_inj_path_obj.input_data_path
        self.train_test_path = data_inj_path_obj.train_test_data_path
        
    def load_data(self):
        try:
            logger.info("Reading input dataset file")

            input_data = pd.read_csv(self.input_path)
            input_data.to_csv(self.train_test_path, index=False)

            logger.info("Data is stored in processed folder")

        except Exception as e:
            logger.exception("Data Injection Exception: %s", e)
            raise CustomException(str(e))

