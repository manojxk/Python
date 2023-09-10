import logging
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.ui import Select

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

# Define a function to select a request
def select_request(jenkins_tag_name, microservice, environment):
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

        # Hold Request
        try:
            hold_request_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[@data-method='put' and @rel='nofollow']/img[@alt='Btn-hold-request']/parent::a")))
            hold_request_button.click()
            logging.info("Request hold")
        except Exception as e:
            logging.warning("Didn't execute hold request")

        # Click "9.1 step off"
        try:
            step = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "tr.step.different_level_from_previous.incomplete_step.procedure_step td[title='9.1 step off']")))
            logging.info(f"Clicked the 9.1 step off: {step.text}")
            step.click()
        except Exception as e:
            logging.warning("Didn't click the 9.1 step off")

        # Promote to Next Env
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td[title='Promote to Next Environment']"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "st_automation"))).click()

        # Additional steps here (adjust as needed)

        # Save data in Excel
        rlm = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='argument_10243']")))
        append_to_excel(microservice, jenkins_tag_name, rlm.text)
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
    select_request(jenkins_tag_name, microservice, "UAT1")
