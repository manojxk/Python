from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    wait = WebDriverWait(driver, 600)
    element = wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, "(//*[@class='state completeRequestStep'])[10]"), "Complete"))
    
    # Perform actions after "Complete" text is present
    promote_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td[title='Promote to Next Environment']")))
    promote_button.click()
    
    st_automation_button = wait.until(EC.presence_of_element_located((By.ID, "st_automation")))
    st_automation_button.click()
    
    rlm = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='argument_10243']")))
    append_to_excel(microservice, jenkins_tag_name, rlm.text)

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()  # Close the driver when done
