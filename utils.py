from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import csv
import time

class LinkProcessor:
    def __init__(self, links_file, status_file='link_status.json'):
        self.links_file = links_file
        self.status_file = status_file
        self.status_dict = self.load_status()
        self.driver = self.setup_driver()

    def setup_driver(self):
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # options.add_argument('--headless')  # Uncomment to run headless
        return webdriver.Chrome(options=options)

    def load_status(self):                                      #TODO: make this work with a CSV or first dump all linke into "pending"
        try:
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "pending": [],
                "executed": [],
                "skipped": []
            }

    def save_status(self):
        with open(self.status_file, 'w') as f:
            json.dump(self.status_dict, f, indent=4)

    def load_links(self):
        with open(self.links_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header if exists                                                  #TODO: Dont't understand howw this works
            return [row[0] for row in reader]

    def process_links(self):
        links = self.load_links()
        
        for link in links:
            if link in self.status_dict["executed"] or link in self.status_dict["skipped"]:         #TODO: This feels redundand
                continue

            try:
                self.process_single_link(link)
            except Exception as e:
                print(f"Error processing {link}: {str(e)}")
                self.status_dict["pending"].append(link)
                self.save_status()

    def process_single_link(self, link):
        try:
            # Open the link
            self.driver.get(link)

            # Wait for page to load (adjust timeout as needed)
            wait = WebDriverWait(self.driver, 10)

            # Check Button A (adjust selector and condition as needed)
            button_a = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="status_10979244011"]')))
            
            # Example condition: check if button text contains certain words
            if button_a.text.lower() in ["Success", "Executing", "Publishing"]:
                print(f"Skipping {link} - condition not met")
                self.status_dict["pending"].remove(link)
                self.status_dict["executed"].append(link)
                return
            elif button_a.text.lower() in ["Waiting for Dependencies"]:
                print(f"Skipping {link} - condition not met")
                self.status_dict["skipped"].append(link)
                self.status_dict["pending"].remove(link)
                return

            # Click Button A and wait for page load
            button_a.click()
            time.sleep(2)  # Allow page to load
                                                                        #TODO: Here also handle the pesky loading page or Error page
            # Find and click Button B
            button_b = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="status_10979244011"]')))
            button_b = button_a.text
            button_b.click()

            # Mark as executed
            print(f"Successfully processed {link}")
            self.status_dict["executed"].append(link)
            if link in self.status_dict["pending"]:
                self.status_dict["pending"].remove(link)

        except TimeoutException:
            print(f"Timeout on {link}")
            self.status_dict["pending"].append(link)
        except NoSuchElementException:
            print(f"Element not found on {link}")
            self.status_dict["skipped"].append(link)
        finally:
            self.save_status()

    def cleanup(self):
        self.driver.quit()
