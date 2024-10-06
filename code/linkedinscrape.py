import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import random
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException


def log_in(driver,account,key):
    try:
        driver.find_element(By.CSS_SELECTOR, "body > nav > div > a.nav__button-secondary.btn-secondary-emphasis.btn-md").click()
        pass
    except NoSuchElementException:
        driver.find_element(By.CSS_SELECTOR, "body > nav > div > a.nav__button-secondary.btn-secondary-emphasis.btn-sm.ml-3").click()
    time.sleep(0.5)

    account_id = driver.find_element(By.CSS_SELECTOR, "input[name='session_key']")
    account_id.send_keys(account)
    account_keys = driver.find_element(By.CSS_SELECTOR, "input[name='session_password']")
    account_keys.send_keys(key)
    driver.find_element(By.CSS_SELECTOR, "#organic-div > form > div.login__form_action_container > button").click()
    time.sleep(60)
    return None

def search_jobs(driver,job):
    driver.find_element(By.CSS_SELECTOR, "#global-nav > div > nav > ul > li:nth-child(3) > a > div > div > li-icon > svg > path").click()
    time.sleep(1)
    search_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[id^='jobs-search-box-keyword-id-ember']"))
    )
    search_area.send_keys(job)
    search_area.send_keys(Keys.RETURN)
    time.sleep(2)
    return None

def get_job_detail(driver, job_element):
    job_detail1 = []
    job_detail2 = []
    try:
        clickable_element = job_element.find_element(By.XPATH, './ancestor::span')
        clickable_element.click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="t-black--light mt2"]'))
        )
        detail1 = driver.find_elements(By.XPATH, '//div[@class="t-black--light mt2"]//span[@class="tvm__text tvm__text--low-emphasis" and not(contains(text(), "·"))]')
        detail2 = job_element.find_elements(By.XPATH, '//div[@class="mt2 mb2"]//li/span/span[not(contains(@class, "white-space-pre"))]')
        for i in detail1:
            job_detail1.append(i.text)
        for i in detail2:
            job_detail2.append(i.text)
    except ElementClickInterceptedException:
        try:
            job_element.click()
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return job_detail1, job_detail2

def get_job_skills_salary(driver,job_element):
    skills = []
    try:
        shortskill = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button > a[class^='app-aware-link']")))
        shortskill.click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "section[class^='ph5']>div>button>span[class='artdeco-button__text']").click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "artdeco-modal__content ember-view job-details-skill-match-modal__container")]')) 
        )
        time.sleep(3)
        skills_elements = driver.find_elements(By.XPATH, '//ul[@class="job-details-skill-match-status-list"]/li/div/div[2]')
            
        for skill in skills_elements:
            skills.append(skill.text)
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Dismiss"]'))
        )
        close_button.click()
        job_salary = driver.find_element(By.CSS_SELECTOR, 'div[class="mt4"]>p').text
    except NoSuchElementException:
        job_salary = 0
    except Exception as e:
        print(f"Error: {e}")
    return skills, job_salary

def write_csv(data,job,header):
    data.insert(loc=0, column='search_key', value=job)
    data.to_csv('{}.csv'.format(job), mode='a+', index=False, header=header,sep=',')
    return None

def job_scraper(driver):
    job_information = pd.DataFrame()
    jobs_and_companies_list = []
    jobs_details = []
    jobs_skills = []
    jobs_salary = []
    try:
        previous_length = 0
        while True:
            jobs_names = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[aria-hidden="true"] strong'))
            )
            company_names = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[class^="job-card-container__primary-description"]'))
            )
            job_locations = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class^='artdeco-entity-lockup__caption ember-view'] > ul > li"))
            )
            if len(jobs_names) == len(company_names):
                for job, company, location in zip(jobs_names, company_names, job_locations):
                    try:
                        job_name = job.text
                        company_name = company.text
                        job_location = location.text
                        if (job_name, company_name, job_location) not in jobs_and_companies_list:
                            job_detail1, job_detail2 = get_job_detail(driver, job)
                            skill,salary = get_job_skills_salary(driver,job)
                            jobs_skills.append(skill)
                            jobs_salary.append(salary)
                            jobs_details.append(tuple([job_detail1,job_detail2]))
                            jobs_and_companies_list.append((job_name, company_name, job_location))
                    except Exception as e:
                        continue  
            current_length = len(jobs_and_companies_list)
            if current_length == previous_length:
                break
            previous_length = current_length
            try:
                left_scrollable_div = driver.find_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div")
                scroll_amount = 500
                driver.execute_script("arguments[0].scrollTop += arguments[1];", left_scrollable_div, scroll_amount)
            except Exception as e:
                print(f"Error: {e}")
                break
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
    try:
        job_information["job_name"] = [job[0] for job in jobs_and_companies_list]
        job_information["company_name"] = [job[1] for job in jobs_and_companies_list]
        job_information["job_location"] = [job[2] for job in jobs_and_companies_list]
        job_information["location"] = [detail[0] for detail in jobs_details]
        job_information["location"] = [detail[0][0] for detail in jobs_details]
        job_information["post_time"] = [detail[0][1] for detail in jobs_details]
        job_information["salary"] = jobs_salary
        job_information["others"] = [detail[1] for detail in jobs_details]
        job_information["skills"] = [skill for skill in jobs_skills]
    except Exception as e:
        print(f"Error: {e}")
    return job_information

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.linkedin.com')
time.sleep(1)

account = ""
key = ""
log_in(driver,account,key)

job_list = ["consulting","data scientist","business analyst","data analyst","marketing","sales","researcher","risk analyst"]
for job in job_list:
    page = 1
    search_jobs(driver,job)
    time.sleep(5)
    while True:
        job_information = job_scraper(driver)
        if page == 1:
            write_csv(job_information,job,True)
        else:
            write_csv(job_information,job,False)
        page += 1
        try:
            driver.find_element(By.CSS_SELECTOR, f"button[aria-label='Page {page}']").click()
        except NoSuchElementException:
            print(f"{job} finished")
            break
        except Exception as e:
            print(f"{job} page {page} ERROE: {e} ")
            continue
        time.sleep(5)
    time.sleep(100)
