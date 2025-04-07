import os

CONFIG_PATH = "config/config.yaml"

####################  Data Ingestion Config   #######################

RAW_DATA_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DATA_DIR, "raw_data.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DATA_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DATA_DIR, "test.csv")


####################  Data Preprocessing Config   #######################

PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR,"processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR,"processed_test.csv")


####################  Model Training Config   #######################

MODEL_DIR = "artifacts/model"