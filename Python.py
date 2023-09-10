import logging
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utils import append_to_excel, append_to_excel_for_rlm_ids

# Configure logging
logging.basicConfig(filename='selenium_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a function for login
def login(driver, username, password):
    try:
        driver.get("https://releaseorchestrationdeployment.citigroup.net/brpm/")
        driver.find_element(By.ID, "user_login").send_keys(username)
        driver.find_element(By.ID, "user_password").send_keys(password)
        driver.find_element(By.NAME, "commit").click()
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        raise

# Define a function to perform the check
def check(jenkins_tag_name, microservice):
    try:
        # Set up Chrome driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        svc = webdriver.ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc, options=chrome_options)

        # Remove implicit wait and use WebDriverWait instead
        wait = WebDriverWait(driver, 15)

        # Login
        login(driver, "ms59214", "Sunita@9791")

        # Navigate to the desired page
        driver.get("https://releaseorchestrationdeployment.citigroup.net/brpm/")

        # Wait for and interact with elements
        wait.until(EC.presence_of_element_located((By.ID, "q"))).send_keys(jenkins_tag_name)
        wait.until(EC.element_to_be_clickable((By.ID, "generic_search_button"))).click()

        # Select correct tag and env from table
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='request_and_calendar']/table/tbody/tr")))
        jenkins_target = f"EB_{jenkins_tag_name}"

        for row in rows:
            jenkins = row.find_element(By.XPATH, "./td[3]").text
            env = row.find_element(By.XPATH, "./td[9]").text
            position = jenkins.find(jenkins_tag_name)
            if position != -1 and env == "UAT1":
                link = row.find_element(By.XPATH, "./td[1]")
                link.click()
                break

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td[title='Promote to Next Environment']"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "st_automation"))).click()

        rlm = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='argument_10243']")))
        append_to_excel(microservice, jenkins_tag_name, rlm.text)
        
        # Log that data has been saved in Excel
        logging.info(f"Data saved in Excel for {microservice}, {jenkins_tag_name}")

        # Close the driver gracefully
        driver.quit()

    except Exception as e:
        logging.error(f"Error processing {microservice}, {jenkins_tag_name}: {str(e)}")
        pass  # Continue processing other records even if there's an error

# Read data from Excel file
df = pd.read_excel("/Users/ms59214/Desktop/Selenium/Manoj - CVM tags jenkins.xlsx", sheet_name="Main_For_Deploy")
jenkins = df["Last success IUT Tag"].tolist()
ms = df["Microservice Name"].tolist()

# Iterate through the data
for microservice, jenkins_tag_name in zip(ms, jenkins):
    logging.info(f"Processing {microservice}, {jenkins_tag_name}")
    check(jenkins_tag_name, microservice)
