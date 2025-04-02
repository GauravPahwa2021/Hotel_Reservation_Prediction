import os
import sys
import yaml
from src.logger import logger
from src.custom_exception import CustomException
import pandas as pd

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path")
        
        with open(file_path,"r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Succesfully read the YAML file")
            return config
    
    except Exception as e:
        logger.error("Error while reading YAML file")
        raise CustomException(e,sys)
    

def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data {e}")
        raise CustomException(e,sys)