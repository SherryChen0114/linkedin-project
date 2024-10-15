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

def job_ave_salary (dataframe):
    '''
    Filter out rows: salary_yr is 0 or internship_flag is 1
    '''
    dataframe['salary_yr'] = dataframe['salary_yr'].astype(str)
    dataframe['salary_yr'] = dataframe['salary_yr'].str.replace(',', '', regex=True)
    dataframe['salary_yr'] = pd.to_numeric(dataframe['salary_yr'])
    filtered_data = dataframe[(dataframe['salary_yr'] > 0) & (dataframe['full_time'] == 1)]
    average_salary = filtered_data.groupby('search_key')['salary_yr'].mean()
    
    return average_salary

def plot_average_salary(average_salary):
    '''
    Plot the bar chart for average salary
    '''
    average_salary.plot(kind='bar', figsize=(10, 6))
    plt.title('Average Yearly Salary for Each Full-time Job Position')
    plt.xlabel('Job_Position')
    plt.ylabel('Average Yearly Salary')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    save_graph(OUTPUT_DIR, 'average_salary.jpg') 

def is_valid_state(state):
    pattern = r'^[A-Z]{2}$'
    return bool(re.match(pattern, state))

def average_salary_by_state(dataframe):
    dataframe['salary_yr'] = dataframe['salary_yr'].astype(str)
    dataframe['salary_yr'] = dataframe['salary_yr'].str.replace(',', '', regex=True)
    dataframe['salary_yr'] = pd.to_numeric(dataframe['salary_yr'])

    filtered_data = dataframe[(dataframe['salary_yr'] > 0) & (dataframe['full_time'] == 1)]
    valid_states_data = filtered_data[filtered_data['state'].apply(is_valid_state)]
    avg_salary_by_state = valid_states_data.groupby('state')['salary_yr'].mean().sort_values(ascending=False)
    return avg_salary_by_state

def plot_avg_salary_by_state(avg_salary_by_state):
    avg_salary_by_state.plot(kind='bar', figsize=(12, 6), color='skyblue')
    plt.title('Average Full-Time Salary by State')
    plt.xlabel('State')
    plt.ylabel('Average Salary (Yearly)')
    plt.xticks(rotation=45)
    plt.tight_layout()  
    save_graph(OUTPUT_DIR, 'avg_salary_by_state.jpg')

def ave_salary_by_work_arrangement(dataframe):
    dataframe['salary_yr'] = dataframe['salary_yr'].astype(str)
    dataframe['salary_yr'] = dataframe['salary_yr'].str.replace(',', '', regex=True)
    dataframe['salary_yr'] = pd.to_numeric(dataframe['salary_yr'])

    filtered_data = dataframe[(dataframe['salary_yr'] > 0) & (dataframe['full_time'] == 1)]
    avg_on_site = filtered_data[filtered_data['on_site_flag'] == 1]['salary_yr'].mean()
    avg_remote = filtered_data[filtered_data['remote_flag'] == 1]['salary_yr'].mean()
    avg_hybrid = filtered_data[filtered_data['Hybrid_flag'] == 1]['salary_yr'].mean()
    avg_salaries = {
        'Work Arrangement': ['On-site', 'Remote', 'Hybrid'],
        'Average Salary': [avg_on_site, avg_remote, avg_hybrid]
    }
    avg_salaries_df = pd.DataFrame(avg_salaries)
    return avg_salaries_df

def plot_salary_by_work_arrangement(avg_salaries):
    labels = avg_salaries['Work Arrangement']
    salaries = avg_salaries['Average Salary']

    plt.bar(labels, salaries, color='skyblue')
    plt.title('Average Full-Time Salary by Work Arrangement')
    plt.xlabel('Work Arrangement')
    plt.ylabel('Average Yearly Salary')
    plt.tight_layout()  
    save_graph(OUTPUT_DIR, 'salary_by_work_arrangement.jpg')



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

    average_salary = job_ave_salary(cleaned_data)
    write_csv(os.path.join(OUTPUT_DIR, 'average_salary_by_job.csv'), average_salary.reset_index())
    plot_average_salary(average_salary)
 
    avg_salaries = ave_salary_by_work_arrangement(cleaned_data)
    write_csv(os.path.join(OUTPUT_DIR, 'average_salary_by_arrangement.csv'), avg_salaries.reset_index())
    plot_salary_by_work_arrangement(avg_salaries)
  
    avg_salary_by_state = average_salary_by_state(cleaned_data)
    write_csv(os.path.join(OUTPUT_DIR, 'average_salary_by_state.csv'), avg_salary_by_state.reset_index())
    plot_avg_salary_by_state(avg_salary_by_state)