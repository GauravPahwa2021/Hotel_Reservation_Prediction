import os

CONFIG_PATH = "config/config.yaml"

####################  Data Ingestion Config   #######################

RAW_DATA_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DATA_DIR, "raw_data.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DATA_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DATA_DIR, "test.csv")