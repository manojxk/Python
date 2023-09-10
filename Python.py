import time
import logging
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utils import append_to_excel, append_to_excel_for_rlm_ids

# Configure logging
logging.basicConfig(filename='selenium_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login(username, password):
    # Add your login logic here
    pass

def select_request(jenkins_tag_name, microservice, environment):
    driver = webdriver.Chrome(executable_path=binary_path)

    try:
        login("ms59214", "Sunita@9791")
        driver.find_element(By.ID, "q").send_keys(jenkins_tag_name)
        driver.find_element(By.ID, "generic_search_button").click()

        # Wait for the table to load
        wait = WebDriverWait(driver, 10)
        rows = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@id='request_and_calendar']/table/tbody/tr")))

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
            logging.info(f"Request hold for {microservice}: {jenkins_tag_name}")
        except Exception as e:
            logging.error(f"Error holding request for {microservice}: {jenkins_tag_name} - {str(e)}")

        # Click "9.1 step off"
        try:
            step_id = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tr.step.different_level_from_previous.incomplete_step.procedure_step"))).text.split()
            step_id = step_id[4]
            step_path = f"step_{step_id}_should_execute"
            step = wait.until(EC.element_to_be_clickable(
                (By.ID, step_path)))
            logging.info(f"Clicking 9.1 step off for {microservice}: {jenkins_tag_name}")
            if step.text == "ON":
                step.click()
        except Exception as e:
            logging.error(f"Error clicking 9.1 step off for {microservice}: {jenkins_tag_name} - {str(e)}")

        # Promote to Next Env
        driver.find_element(
            By.CSS_SELECTOR, "td[title='Promote to Next Environment']").click()
        # Add WebDriverWait if needed for elements in this section

        # Start Request
        start_request_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[@data-method='put' and @rel='nofollow']/img[@alt='Btn-start-request']/parent::a")))
        start_request_button.click()

        # Click the green tick
        complete_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='complete' and @title='Complete' and @type='image' and @alt='Complete']")))
        complete_button.click()

        try:
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, "(//*[@class='state completeRequestStep'])[10]"), "Complete"))

            driver.find_element(
                By.CSS_SELECTOR, "td[title='Promote to Next Environment']").click()
            rlm = driver.find_element(By.XPATH, "//*[@id='argument_10243']")
            append_to_excel(microservice, jenkins_tag_name, rlm.text)

        except Exception as e:
            logging.error(f"Error in processing {microservice}: {jenkins_tag_name} - {str(e)}")

    except Exception as e:
        logging.error(f"Error processing {microservice}: {jenkins_tag_name} - {str(e)}")

    finally:
        driver.close()

# Rest of your code for reading Excel and iterating through data

if __name__ == "__main__":
    df = pd.read_excel(
        "/Users/ms59214/Desktop/Selenium/Manoj - CVM tags jenkins.xlsx", sheet_name="Main_For_Deploy")

    jenkins = df["Last success IUT Tag"].tolist()
    ms = df["Microservice Name"].tolist()

    start_time = time.time()

    for microservice, jenkins_tag_name in zip(ms, jenkins):
        print(microservice, jenkins_tag_name)
        select_request(jenkins_tag_name, microservice, "UAT1")

    end_time = time.time()

    print(f"time taken {end_time-start_time}")
