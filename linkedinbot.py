
#--------------------------------------------------------------------------------------------#

# Replace with your LinkedIn credentials
linkedin_email = 'abc@xyz.com'
linkedin_password = 'password'

#Modify according to your needs.
#text_message - Add a message to sent along with connection request. Serves the 
text_message = "Hey, I am XYZ. Glad to connect with you"
no_of_pages = 1
keywords = "Quant Hiring"

# Replace with the path to your ChromeDriver
chromedriver_path = '/path/to/chromedriver'


#---------------------------------------------------------------------------------------------#

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Selenium WebDriver
driver = webdriver.Chrome(chromedriver_path)
driver.get('https://www.linkedin.com/')

# Log in to LinkedIn
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="session_key"]'))
)
email_input = driver.find_element(By.XPATH, '//input[@id="session_key"]')
email_input.send_keys(linkedin_email)
password_input = driver.find_element(By.XPATH, '//input[@id="session_password"]')
password_input.send_keys(linkedin_password)
password_input.send_keys(Keys.RETURN)

#Iterate therough the number of pages assigned
for page in (1, no_of_pages):
    print("Page - " + str(page))
    query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
    driver.get(query_url)
    #wait for some time
    time.sleep(1)
    linkedin_urls = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
    for result in linkedin_urls:
        username = result.text.split('\n')[0]
        connection_action = result.find_elements(By.CLASS_NAME, 'artdeco-button__text')
        if connection_action:
            connection = connection_action[0]
        else:
            print()
        if connection.text == 'Connect':
            try:
                time.sleep(1)
                connection.click()
                if driver.find_elements(By.CLASS_NAME, 'artdeco-button--secondary')[0].is_enabled():
                        driver.find_elements(By.CLASS_NAME, 'artdeco-button--secondary')[0].click()
                        time.sleep(2)
                        driver.find_element(By.CLASS_NAME, 'connect-button-send-invite__custom-message').send_keys(text_message)
                        driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].click()
                print(username + " : Connected")
            except Exception as e :
                print(username + " : Not Connected")
        if connection.text == 'Pending':
             print(username + " : Pending")
driver.quit()