# Promote to Next Env
promote_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td[title='Promote to Next Environment']")))
promote_button.click()

st_automation_button = wait.until(EC.presence_of_element_located((By.ID, "st_automation")))
st_automation_button.click()

argument_link = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@id='argument_10241']//a")))
argument_link.click()

dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "script_argument_10241"))))
dropdown.select_by_index(11)
dropdown.select_by_index(18)

save_data_button = wait.until(EC.presence_of_element_located((By.ID, "save_data_retriever")))
save_data_button.click()

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='button' and @value='Save Step']"))).click()
