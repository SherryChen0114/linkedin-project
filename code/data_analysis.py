import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
from clean_data import data_clean
from clean_data import  write_csv

def save_graph(path, name):
    output_path = os.path.join(path, name)
    plt.savefig(output_path)
    return None

def count_position(dataframe):
    '''
    Count the occurrences of different search_key values (jon title)
    '''
    search_key_counts = dataframe['search_key'].value_counts()
    return search_key_counts

def plot_search_key_counts(search_key_counts):
    '''
    Plot the bar chart for search results in different job positions
    ''' 
    search_key_counts.plot(kind='bar', figsize=(10, 6))
    plt.title('Count of Different Positions (search_key)')
    plt.xlabel('Job_Position')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    save_graph(OUTPUT_DIR, 'search_key_counts.jpg') 





if __name__ == "__main__":
    DATA_BASE_DIR = "data"
    DATA_INPUT_DIR = os.path.join(DATA_BASE_DIR, "rawdata")
    csv_files = glob.glob(os.path.join(DATA_INPUT_DIR, "*.csv"))
    OUTPUT_DIR = os.path.join("results")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cleaned_data = data_clean(csv_files)

    search_key_counts = count_position(cleaned_data)
    write_csv(os.path.join(OUTPUT_DIR, 'search_key_counts.csv'), search_key_counts.reset_index())
    plot_search_key_counts(search_key_counts)