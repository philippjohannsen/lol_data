from config import *
from drive import drive_manager






if __name__ == '__main__':
    # when script is run, create the data directory
    RAW_DIR.mkdir(exist_ok=True, parents=True)
    FINAL_DIR.mkdir(exist_ok=True)
    CLEANED_DIR.mkdir(exist_ok=True)

    # download data from drive
    drive_manager(ELIXIR_DRIVE, RAW_DIR)
