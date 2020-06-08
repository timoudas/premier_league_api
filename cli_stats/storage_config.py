import os

class StorageConfig:
    """Class with directory variables to locate folders"""
    STORAGE_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    PARAMS_DIR = STORAGE_BASE_DIR +'/'+ "params"
    STATS_DIR = STORAGE_BASE_DIR +'/'+ "raw_data"
    DB_DIR = STORAGE_BASE_DIR +'/'+ "clean_data"

if __name__ == '__main__':
    print(StorageConfig.STORAGE_BASE_DIR)
    print(StorageConfig.STATS_DIR)