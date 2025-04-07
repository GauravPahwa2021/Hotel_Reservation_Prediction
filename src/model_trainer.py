import os
import sys
import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import *
from scipy.stats import randint

from dotenv import load_dotenv
load_dotenv()

import mlflow
from urllib.parse import urlparse
# import dagshub
# from dagshub import DAGSHUB

# Initialize DagsHub
# dagshub = DAGSHUB(token=os.getenv("DAGSHUB_TOKEN")) 
# dagshub.init(repo_owner='GauravPahwa2021', repo_name='Hotel_Reservation_Prediction', mlflow=True)
# Set the MLflow tracking URI to DagsHub
# mlflow.set_tracking_uri("https://dagshub.com/GauravPahwa2021/Hotel_Reservation_Prediction.mlflow")


class ModelTraining:

    def __init__(self,train_path,test_path,model_dir):
        self.train_path = train_path
        self.test_path = test_path
        self.model_dir = model_dir

        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        self.model_path = os.path.join(self.model_dir,"light_gbm.pkl")

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data splitted sucefully for Model Training")

            return X_train,y_train,X_test,y_test
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException(e,sys)
        
    
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("Intializing our model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our Hyperparamter tuning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )

            logger.info("Starting our Hyperparamter tuning")

            random_search.fit(X_train,y_train)

            logger.info("Hyperparamter tuning completed")

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best paramters are : {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException(e,sys)
    

    def evaluate_model(self , model , X_test , y_test):
        try:
            logger.info("Evaluating our model")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1 Score : {f1}")

            return {
                "accuracy" : accuracy,
                "precison" : precision,
                "recall" : recall,
                "f1" : f1
            }
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException(e,sys)
        

    def save_model(self,model):
        try:
            logger.info("saving the model")

            joblib.dump(model, self.model_path)

            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error while saving model {e}")
            raise CustomException(e,sys)
    

    def run(self):
        try:
            # mlflow.set_registry_uri("https://dagshub.com/GauravPahwa2021/Hotel_Reservation_Prediction.mlflow")
            # tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            mlflow.set_experiment("Hotel_Reservation_Prediction")

            with mlflow.start_run():
                logger.info("Starting our Model Training pipeline")

                logger.info("Starting our MLFLOW experimentation")

                logger.info("Logging the training and testing dataset to MLFLOW")

                mlflow.log_artifact(self.train_path , artifact_path="datasets")
                mlflow.log_artifact(self.test_path , artifact_path="datasets")

                X_train,y_train,X_test,y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train,y_train)
                metrics = self.evaluate_model(best_lgbm_model,X_test,y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging the model into MLFLOW")
                mlflow.log_artifact(self.model_path)

                logger.info("Logging Params and metrics to MLFLOW")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Logging Model to MLFLOW")
                mlflow.sklearn.log_model(best_lgbm_model, "model") 
                # if tracking_uri_type_store != "file":
                #     # Register the model
                #     mlflow.sklearn.log_model(best_lgbm_model, "model", registered_model_name="LightGBM_Model")
                # else:
                #     mlflow.sklearn.log_model(best_lgbm_model, "model")  

                logger.info("Model Training sucesfullly completed")

        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Failed during model training pipeline" ,  e)
        


if __name__=="__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_DIR)
    trainer.run()
        

    

            