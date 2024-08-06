from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class LogIn:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def select_country(self):
        us_link = self.driver.find_element(By.CLASS_NAME, 'us-link')
        us_link.click()


    def open_sign_in_menu(self):
        account_menu = self.wait.until(EC.element_to_be_clickable((By.ID, 'account-menu-account-button')))
        account_menu.click()
    
    def click_sign_in(self):
        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'c-button-secondary')))
        sign_in_button.click()

    def login(self, username, password):
        email_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'fld-e')))
        email_field.send_keys(username)
        password_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'fld-p1')))
        password_field.send_keys(password)
        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'c-button-secondary')))
        sign_in_button.click()
        self.handle_recovery_prompt()

    def handle_recovery_prompt(self):
        try:
            skip_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cia-cancel')))
            skip_button.click()
        except Exception as e:
            logging.info("Skip button not found or not required: %s", e)
