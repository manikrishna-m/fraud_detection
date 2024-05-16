import os
import sys
import joblib
from dataclasses import dataclass
from pathlib import Path
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# Adding the parent path to sys.path to import CustomException and get_logger
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.exception import CustomException
from src.logger import get_logger
sys.path.pop()  # Remove the added path after import

logger = get_logger()

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = "data/processed/model.pkl"

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.model_path = self.model_trainer_config.trained_model_file_path

    def initiate_model_trainer(self, train_input_array, train_target_array, test_input_array, test_target_array):
        try:
            logger.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_input_array, train_target_array, test_input_array, test_target_array
            )
            logger.info("Data split completed successfully")
            
            models = {
                "Random Forest": RandomForestClassifier(),
            }

            logger.info("Starting model evaluation")
            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models
            )

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            logger.info(f"Best model found: {best_model_name} with score: {best_model_score}")

            if best_model_score < 0.6:
                raise CustomException("No best model found", sys)
            
            logger.info("Saving the best model")
            dir_path = os.path.dirname(self.model_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(self.model_path, "wb") as file_obj:
                joblib.dump(best_model, file_obj)

            logger.info("Evaluating the best model accuracy on test data")
            predicted = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, predicted)
            return accuracy

        except Exception as e:
            logger.exception("Model Trainer Exception: %s", e)
            raise CustomException(str(e))

def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
        report = {}

        for model_name, model in models.items():
            logger.info("Evaluating model: %s", model_name)

            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            test_model_score = accuracy_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            logger.info(f"Model {model_name} scored {test_model_score}")

        return report

    except Exception as e:
        logger.exception("Model Evaluation Exception: %s", e)
        raise CustomException(str(e))
