from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

import time

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_home(self):
        self.driver.get("https://www.bestbuy.com")
        time.sleep(2)
        self.select_country()

    def select_country(self):
        us_link = self.driver.find_element(By.CLASS_NAME, 'us-link')
        us_link.click()
        time.sleep(2)

    def perform_search(self, query):
        search_field = self.driver.find_element(By.ID, 'gh-search-input')
        search_field.send_keys(query)
        time.sleep(2)  # Wait for suggestions to appear

    def check_search_results(self):
        results = self.driver.find_elements(By.CSS_SELECTOR, "ul.list-unstyled.m-none.p-none.border-none.shadow-none li a.text-info.flex.p-100")
        print(f"Found {len(results)} suggestions: {[result.text for result in results]}")
        return results

    def hover_over_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        time.sleep(1)  # Wait for the hover effect to take place
        print("Hovered over element with text:", element.text)

    def get_right_side_content(self):
        right_side_content = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Related Products']").text
        return right_side_content

    def go_to_third_product(self):
        try:
            third_product_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[@class='clamp lines-3 v-text-tech-black suggest-target'])[3]"))
            )
            print(f"Navigating to third product: {third_product_link.text}")
            third_product_link.click()
        except TimeoutException as e:
            print("Timeout: Third product link is not clickable:", e)
            raise e

    def get_price_text_size(self):
        price_element = self.driver.find_element(By.CSS_SELECTOR, ".priceView-hero-price span")
        price_text_size = price_element.value_of_css_property("font-size")
        price_text = price_element.text
        return price_text_size, price_text

    def get_specifications(self):
        try:
            specs_button = self.driver.find_element(By.CSS_SELECTOR, ".c-button-unstyled.specifications-drawer-btn.w-full.flex.justify-content-between.align-items-center.py-200")
            specs_button.click()
            spec_content = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='h-full flex flex-column']"))
            ).text
            print("Specifications section is displayed with content")
            spec_button_close = self.driver.find_element(By.CSS_SELECTOR,"div[class='flex justify-content-between'] button[aria-label='Close']")
            spec_button_close.click()
            return spec_content
        except (TimeoutException, NoSuchElementException) as e:
            print("Specifications section not found")
            raise e
        
    def get_features(self):
        try:                                                            
            features_button = self.driver.find_element(By.CSS_SELECTOR, ".c-button-unstyled.specifications-drawer-btn.w-full.flex.justify-content-between.align-items-center.py-200")
            features_button.click()
            features_content = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='h-full flex flex-column']"))
            ).text
            print("Features section is displayed with content")
            feature_button_close = self.driver.find_element(By.CSS_SELECTOR,"div[class='flex justify-content-between'] button[aria-label='Close']")
            feature_button_close.click()
            return features_content
        except (TimeoutException, NoSuchElementException) as e:
            print("Features section not found")
            raise e

    def get_questions_and_answers(self):
        try:
            qa_element = self.driver.find_element(By.XPATH, "(//span[@class='heading-5'])[1]")
            print("Questions & Answers section is displayed with content")
            return qa_element.text
        except NoSuchElementException as e:
            print("Questions & Answers section not found")
            raise e
