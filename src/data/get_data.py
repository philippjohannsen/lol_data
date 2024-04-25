from .config import DATA_DIR, RAW_DIR, FINAL_DIR, CLEANED_DIR








if __name__ == '__main__':
    # when script is run, create the data directory
    RAW_DIR.mkdir(exist_ok=True, parents=True)
    FINAL_DIR.mkdir(exist_ok=True)
    CLEANED_DIR.mkdir(exist_ok=True)