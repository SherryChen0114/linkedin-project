# Case Study of LinkedIn Job Post for Economics Major

## Data  

In this project, we collected the data from LinkdIn website. And the data involved 8 types of jobs: consulting, data scientist, business analyst, data analyst, marketing, sales, researcher, risk analyst, which are highly related to the economics major. Finally, we totally collected 16354 job positions, including the name of position, location, salary, time post, required skills, work arrangement, and employment types. 

 
### Data Collection Method

We used Selenium to interact with the LinkedIn website, simulating user actions such as logging in, searching, and navigating job listings. Job listings were scraped automatically for each job title, with the data processed iteratively, moving from page to page until all listings for that title were collected. Since LinkedIn provides a maximum of 40 pages of data per search keyword, we used our LinkedIn account to gather additional data, which was merged to create a more comprehensive dataset.

After scraping the data three times, we merged all the collected data and removed duplicate job postings. We then processed key fields such as location, salary, work arrangement, and employment type to generate the final clean_data dataset.

### Limitation of the Data
 
First, LinkedIn restricts the data to a maximum of 40 pages per search keyword, which limits our ability to collect all relevant job postings. This limitation affects our analysis and may introduce bias into the results.

Second, our data collection was limited to LinkedIn. To provide a more comprehensive view, data from other platforms such as Handshake, Indeed, and ZipRecruiter could be included for comparison.

Third, some job postings on LinkedIn contain inaccurate or unrealistic information, such as salary ranges from $1 to $300,000, which can skew the analysis.

Lastly, in our cluster analysis, we used GPT for classification. However, the classification results were not entirely accurate, and we only manually verified a portion of the data.

### Extention of the Data

First, we can expand the size of our dataset to improve the accuracy of our analysis.

Second, in our salary study, we analyzed only the absolute salary values without considering the local cost of living or regional wage levels. Incorporating data such as the Consumer Price Index (CPI) or average regional salary statistics provided by government sources would offer more context to the analysis.

Third, in the salary analysis, we used histograms to represent wage differences across states. A more intuitive approach would be to use a geographical map with heatmaps to visually depict salary variations across regions.

Lastly, in the cluster analysis, we used the K-means method, but the results were highly dependent on the number of clusters, and some clusters were quite similar. For lower-dimensional feature data, alternative clustering methods may provide better results.

### Descriptive Summary
Using our revised dataset along with Pandas and Matplotlib, the results indicated that different search keys produced varying numbers of job listings on LinkedIn. The analysis showed that using "data analyst" as the search key yielded the highest search result of 2,295 listings, whereas "business analyst" generated the lowest result of 1,868 listings.

| Search Key      | Counts |
|-----------------|--------|
| Data Analyst    | 2295   |
| Risk Analyst    | 2117   |
| Consulting      | 2084   |
| Researcher      | 2070   |
| Sales           | 2008   |
| Data Scientist  | 1993   |
| Marketing       | 1918   |
| Business Analyst| 1868   |   



## Salary Analysis
The primary goal of this project was to use the scraped data from LinkedIn to provide economics major students with valuable insights into choosing their careers, job locations.

### Average Salary Analysis
We divided the salary analysis into three parts to examine how job types, job location (at the state level), and work arrangements influenced salary levels for full-time positions.

#### Job Types

The results indicated that data scientists had the highest average salary, earning $121,267.80, while business analysts had the lowest average salary among the eight job titles commonly searched by economics students. Despite having the lowest salary, business analysts were closely followed by marketing and sales positions, showing little difference in average salary.

| Search Key        | Average Salary |
|-------------------|----------------|
| Data Analyst      | 81,569.23       |
| Risk Analyst      | 87,508.73       |
| Consulting        | 101,753.06      |
| Researcher        | 112,241.14      |
| Sales             | 82,339.85       |
| Data Scientist    | 121,267.80      |
| Marketing         | 82,477.87       |
| Business Analyst  | 96,346.48       |

#### Job Locations

When analyzing salaries by state, California (CA) had the highest average salary at $106,932.28, while Kansas (KS) had the lowest at $40,250. Iowa (IA) reported the second-highest average salary at $105,000, which seemed counterintuitive. This may have been due to the limited number of job listings in Iowa, leading to a smaller dataset, or because the jobs listed on LinkedIn for Iowa were predominantly high-paying roles. Incorporating price levels or purchasing power for each state could provide additional context on actual salary levels.

| State | Salary (Yearly) | State | Salary (Yearly) |
|-------|-----------------|-------|-----------------|
| CA    | 106,932.28       | ID    | 81,934.67       |
| IA    | 105,000.00       | RI    | 80,933.33       |
| MT    | 104,217.89       | PA    | 80,222.64       |
| NY    | 103,135.21       | MO    | 79,627.06       |
| DC    | 102,366.82       | CO    | 79,580.59       |
| LA    | 99,107.14        | AZ    | 79,097.53       |
| IL    | 98,382.10        | OR    | 79,087.03       |
| WA    | 95,488.12        | VA    | 78,511.73       |
| GA    | 95,387.64        | UT    | 76,002.18       |
| NJ    | 94,410.91        | MD    | 74,070.76       |
| MN    | 90,923.13        | IN    | 73,251.60       |
| AR    | 90,853.13        | SC    | 72,919.62       |
| DE    | 90,631.43        | ND    | 72,624.00       |
| HI    | 89,910.00        | WI    | 72,383.89       |
| TX    | 87,890.95        | ME    | 70,546.86       |
| NC    | 87,035.55        | MI    | 68,841.55       |
| CT    | 86,618.26        | NM    | 68,000.00       |
| FL    | 83,940.83        | WY    | 68,000.00       |
| WV    | 83,567.86        | NV    | 66,393.75       |
| MA    | 83,349.49        | AL    | 65,682.52       |
| TN    | 82,383.64        | NH    | 63,333.33       |
| OH    | 82,335.94        | AK    | 62,689.00       |
| KY    | 56,871.30        | OK    | 61,102.63       |
| MS    | 55,000.00        | NE    | 52,833.33       |
| VT    | 52,760.00        | KS    | 40,250.00       |

#### Work Arrangement

We also analyzed whether work arrangements affected salary levels. The results suggested that on-site jobs had the lowest average salary at $91,970.53. In contrast, remote and hybrid arrangements showed higher average salaries, with remote jobs averaging $96,039.93 and hybrid jobs averaging $96,368.86. This difference was likely due to companies having lower office-related costs for remote and hybrid jobs.

| Work Arrangement | Average Salary  |
|------------------|-----------------|
| On-site          | 91,970.53        |
| Remote           | 96,039.93        |
| Hybrid           | 96,368.86        |

## Skill Analysis

### Skills Word Cloud Based on Job Types

### K-mean Analysis for Job Types

## Instruction to Rerun
