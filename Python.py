# Start Request
start_request_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-method='put' and @rel='nofollow']/img[@alt='Btn-start-request']/parent::a")))
start_request_button.click()

# Click the green tick
complete_button = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='complete' and @title='Complete' and @type='image' and @alt='Complete']")))
complete_button.click()
