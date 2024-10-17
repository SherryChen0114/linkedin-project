import os
import glob
import pandas as pd
import ast
import re


def data_merge(job_list):
    """This function is used to merge data."""
    dfs = []
    for file in job_list:
        df = pd.read_csv(file)
        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.drop_duplicates(inplace=True)

    return merged_df


def location(df):
    """This function is used to process the location variable in the raw file."""
    df[["city", "state"]] = df["location"].str.extract(r"([^,]+),?\s*([^,]*)")
    return df


def others(others_str):
    """This function is used to process the others variable in the raw file."""
    try:
        other_lists = ast.literal_eval(others_str)  # change string to a list

        if isinstance(other_lists, list):
            non_price_elements = []
            for item in other_lists:
                if not re.match(r"^\$", item):
                    non_price_elements.append(item)
            return non_price_elements
        else:
            return others_str
    except (ValueError, SyntaxError):
        return others_str


def check_keywords(other_lists):
    """This function is used to extract keywords from the others variable in the raw file and generate a series of dummy variables."""
    Internship_flag = 0
    on_site_flag = 0
    remote_flag = 0
    Hybrid_flag = 0
    part_time = 0
    full_time = 0
    if isinstance(other_lists, list):
        for item in other_lists:
            if isinstance(item, str):
                if "internship" in item.lower():
                    Internship_flag = 1
                if "on-site" in item.lower():
                    on_site_flag = 1
                if "remote" in item.lower():
                    remote_flag = 1
                if "hybrid" in item.lower():
                    Hybrid_flag = 1
                if "part-time" in item.lower():
                    part_time = 1
                if "full-time" in item.lower():
                    full_time = 1
        return (
            Internship_flag,
            on_site_flag,
            remote_flag,
            Hybrid_flag,
            part_time,
            full_time,
        )
    else:
        return 0, 0, 0, 0, 0, 0


def write_csv(path, dataframe):
    """This function is used to write data into a CSV file."""
    dataframe.to_csv(path, mode="w+", index=False, encoding="utf-8")


def get_salary(dataframe):
    """This function is used to process the salary variable in the raw data."""
    salaries = dataframe["salary"]
    salary_yr = []
    for salary in salaries:
        if (len(str(salary)) > 1) & ("/yr" in str(salary)) & ("£" not in str(salary)):
            end = salary.index("/yr")
            s = salary[:end]
            try:
                start = salary.index("$")
                s = s[start + 1 :]
                salary_yr.append(s)
            except:
                salary_yr.append(s)
        else:
            s = 0
            salary_yr.append(s)
    dataframe["salary_yr"] = salary_yr
    return dataframe


def data_clean(files):
    """This function is primarily used to execute the entire data cleaning process."""
    raw_csv = data_merge(files)
    change_location = location(raw_csv)
    cleaned_data = get_salary(change_location)
    cleaned_data = change_location
    cleaned_data["others"] = change_location["others"].apply(others)
    cleaned_data["internship_flag"] = change_location["others"].apply(
        lambda x: check_keywords(x)[0]
    )
    cleaned_data["on_site_flag"] = change_location["others"].apply(
        lambda x: check_keywords(x)[1]
    )
    cleaned_data["remote_flag"] = change_location["others"].apply(
        lambda x: check_keywords(x)[2]
    )
    cleaned_data["Hybrid_flag"] = change_location["others"].apply(
        lambda x: check_keywords(x)[3]
    )
    cleaned_data["part_time"] = change_location["others"].apply(
        lambda x: check_keywords(x)[4]
    )
    cleaned_data["full_time"] = change_location["others"].apply(
        lambda x: check_keywords(x)[5]
    )
    cleaned_data = cleaned_data.reset_index(drop=True)
    return cleaned_data


if __name__ == "__main__":
    BASE_DIR = "data"
    INPUT_DIR = os.path.join(BASE_DIR, "rawdata")
    OUTPUT_DIR = os.path.join(BASE_DIR, "Revised")
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, "merged.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    cleaned_data = data_clean(csv_files)
    write_csv(OUTPUT_PATH, cleaned_data)
