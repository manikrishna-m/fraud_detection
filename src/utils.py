import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.logger import get_logger
from src.data_components.data_injection_scripts import DataInjection
from src.data_components.data_preprocessing_scripts import DataProcessing
from src.data_components.model_evaluation_scripts import ModelTrainer

sys.path.pop()

logger = get_logger()

if __name__ == "__main__":
    try:
        logger.info("Data Injection is started")
        data_injection = DataInjection()
        data_injection.load_data()
        logger.info("Data Injection is finished")

        logger.info("Data Preprocessing pipelines is started")
        data_processing = DataProcessing()
        train_input_arr, train_target_arr, test_input_arr, test_target_arr, _ = data_processing.data_preprocessing()
        logger.info("Data preprocessing pipelines is finished")

        logger.info("Model Building is started")
        model_trainer = ModelTrainer()
        best_accuracy = model_trainer.initiate_model_trainer(train_input_arr, train_target_arr, test_input_arr, test_target_arr)
        logger.info(f"Best model accuracy is {best_accuracy}")
        logger.info("Model building is finished")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
