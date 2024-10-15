import os
import pandas as pd
import numpy as np
import csv
import glob
from math import pi
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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

def read_classified_skills(name):
    df = pd.read_csv(name)
    return df

def classify_skills(skills):
    professional_count = 0
    soft_count = 0
    coding_count = 0
    cleaned_skills = clean_skill(skills)
    if isinstance(cleaned_skills, list):
        for skill in cleaned_skills:
            skill_type = skill_type_mapping.get(skill, None)
            if skill_type == 'professional':
                professional_count += 1
            elif skill_type == 'soft':
                soft_count += 1
            elif skill_type == 'coding':
                coding_count += 1
    return professional_count, soft_count, coding_count

def generate_classify_variables(based_df,classify_df):
    df = based_df
    skill_type_mapping = classify_df.set_index('skills')['skill_type'].to_dict()
    df[['professional', 'soft', 'coding']] = based_df['skills'].apply(lambda x: pd.Series(classify_skills(x)))
    return df

def decide_clustering_num(features,output_path):
    path = os.path.join(output_path, "elbow_method.png")
    SSE = []
    k_list = range(1,15)
    for k in k_list:
        clustering=KMeans(n_clusters=k,n_init=10)
        clustering.fit(features)
        SSE.append(clustering.inertia_)
    plt.xlabel("K")
    plt.ylabel("SSE")
    plt.plot(k_list,SSE,"o-")
    plt.savefig(path)
    return None

def radar_chart(centers, output_path, dimensions):
    num_clusters = centers.shape[0]
    num_dimensions = centers.shape[1]
    angles = [n / float(num_dimensions) * 2 * pi for n in range(num_dimensions)]
    angles += angles[:1] 
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i in range(num_clusters):
        values = centers[i].tolist()
        values += values[:1] 
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Cluster {i}')
        ax.fill(angles, values, alpha=0.25)
    plt.title("Cluster Centers Radar Chart", size=16, color='black', y=1.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions)
    ax.set_yticklabels([])
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    path = os.path.join(output_path, "cluster_radar_chart.png")
    plt.savefig(path, dpi=300)
    return None

def find_major_cluster_per_search_key(df):
    cluster_distribution = df.groupby(['search_key', 'cluster']).size().unstack(fill_value=0)
    major_clusters = cluster_distribution.idxmax(axis=1)
    result_df = cluster_distribution.copy()
    result_df['cluster'] = major_clusters
    result_df = result_df.reset_index()
    return result_df

def k_means_analysis(df,output_path):
    features = df[['professional', 'soft', 'coding']]
    features = StandardScaler().fit_transform(features)
    decide_clustering_num(features,output_path)
    k = 5
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)
    fig = plt.figure(figsize=(10, 8))
    centers = kmeans.cluster_centers_
    radar_chart(centers, output_path, ['Professional', 'Soft', 'Coding'])
    major_cluster_df = find_major_cluster_per_search_key(df)
    return major_cluster_df

if __name__ == "__main__":
    DATA_BASE_DIR = "data"
    DATA_INPUT_DIR = os.path.join(DATA_BASE_DIR, "rawdata")
    csv_files = glob.glob(os.path.join(DATA_INPUT_DIR, "*.csv"))
    OUTPUT_DIR = os.path.join("results")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cleaned_data = data_clean(csv_files)
    unique_skill_words = get_skill_count("all", cleaned_data)
    write_dic_to_csv(os.path.join(OUTPUT_DIR, "unique_word.csv"),unique_skill_words)
    classified_skills = read_classified_skills(os.path.join(OUTPUT_DIR, "classified_Skills.csv"))
    skill_type_mapping = classified_skills.set_index('skills')['skill_type'].to_dict()
    classified_data = generate_classify_variables(cleaned_data,classified_skills)
    write_csv(os.path.join(OUTPUT_DIR, "classified_data.csv"),classified_data)
    cluster_results = k_means_analysis(classified_data,OUTPUT_DIR)
    write_csv(os.path.join(OUTPUT_DIR, "cluster_results.csv"),cluster_results)