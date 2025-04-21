import os
import pandas as pd
import selenium
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_job_list():
    return pd.read_csv(jobs_path).to_list()


class SeleniumClass():
    def __init__(self):
        chrome_options = Options()
        # service = Service(executable_path="path/to/chromedriver")  # Replace with the actual path to chromedriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.link = None

        def evaluate_job(self, link):
            self.link = link
            self.driver.get(self.link)
            self.driver.implicitly_wait(10)
            label_text = self.driver.find_element("xpath", "//a[@id='status_10845146127']").text
            if label_text in executing_labels:
                return True
            else: 
                return False

        def prioritize_job(self):
            self.driver.find_element("xpath", "//a[@id='status_10845146127']").click()
            self.driver.implicitly_wait(10)
            try:
                button = self.driver.find_element("xpath", "//*[@id='actionsSection']")
                if button.is_enabled():
                    button.click()
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Error occurred: {e}")
                return False

def status_report():
    return print(
        f"Total Jobs: {len(get_job_list())}, \nCompleted Jobs: {len(completed_jobs)}, \nPending Jobs: {len(pending_jobs)}"
    )
