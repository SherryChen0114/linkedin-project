import os
import pandas as pd
import numpy as np
import csv
import glob
from clean_data import data_clean
from clean_data import write_csv
from data_analysis import get_skill_count
from data_analysis import clean_skill

def write_dic_to_csv(path,dic):
    with open(path, mode='w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["skills", "count"])
        for key, value in dic.items():
            writer.writerow([key, value])

if __name__ == "__main__":
    DATA_BASE_DIR = "data"
    DATA_INPUT_DIR = os.path.join(DATA_BASE_DIR, "rawdata")
    csv_files = glob.glob(os.path.join(DATA_INPUT_DIR, "*.csv"))
    OUTPUT_DIR = os.path.join("results")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cleaned_data = data_clean(csv_files)
    unique_skill_words = get_skill_count("all", cleaned_data)
    write_dic_to_csv(os.path.join(OUTPUT_DIR, "unique_word.csv"),unique_skill_words)