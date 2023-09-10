export CITI_USERNAME=your_username
export CITI_PASSWORD=your_password
import os

# Get login credentials from environment variables
citi_username = os.environ.get("CITI_USERNAME")
citi_password = os.environ.get("CITI_PASSWORD")

# Define a function for login
def login(driver):
    try:
        driver.get("https://releaseorchestrationdeployment.citigroup.net/brpm/")
        driver.find_element(By.ID, "user_login").send_keys(citi_username)
        driver.find_element(By.ID, "user_password").send_keys(citi_password)
        driver.find_element(By.NAME, "commit").click()
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        raise

# Rest of your code...
