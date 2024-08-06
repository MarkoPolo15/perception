import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def open_sign_in_menu(self):
        account_menu = self.driver.find_element(By.ID, 'account-menu-account-button')
        account_menu.click()
        time.sleep(2)
    
    def click_sign_in(self):
        sign_in_button = self.driver.find_element(By.CLASS_NAME, 'c-button-secondary')
        sign_in_button.click()
        time.sleep(2)

    def login(self, username, password):
        email_field = self.driver.find_element(By.ID, 'fld-e')
        email_field.send_keys(username)
        password_field = self.driver.find_element(By.ID, 'fld-p1')
        password_field.send_keys(password)
        sign_in_button = self.driver.find_element(By.CLASS_NAME, 'c-button-secondary')
        sign_in_button.click()
        time.sleep(5)  # Wait for the login to complete
        self.handle_recovery_prompt()

    def handle_recovery_prompt(self):
        try:
            skip_button = self.driver.find_element(By.CLASS_NAME, 'cia-cancel')
            skip_button.click()
            time.sleep(2)
        except Exception as e:
            print("Skip button not found or not required: ", e)

    def perform_search(self, query):
        search_field = self.driver.find_element(By.ID, 'gh-search-input')
        search_field.send_keys(query + Keys.RETURN)
        time.sleep(3)

    def check_search_results(self):
        results = self.driver.find_elements(By.CSS_SELECTOR, ".sku-title > h4 > a")
        for result in results:
            assert "hello kitty" in result.text.lower(), f"'{result.text}' does not contain 'hello kitty'"

    def hover_and_check_product_for_section(self):
        # Creating an instance of ActionChains
        action = ActionChains(self.driver)

        # Locating the main menu (parent element)
        products_for_section = self.driver.find_element(By.CSS_SELECTOR, ".gh-search-nav-bar")

        # Locating the suggestions dropdown elements (child elements)
        suggestions = self.driver.find_elements(By.CSS_SELECTOR, '.suggestions-dropdown .suggestions-box ul li')

        # Store the initial content of the "products for" section
        initial_content = products_for_section.text

        hovered_suggestions = []

        # Iterate over the suggestions and check if the content changes on hover
        for suggestion in suggestions:
            # Hover over each suggestion
            action.move_to_element(suggestion).perform()

            # Adding a small wait to ensure the content is updated
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".gh-search-nav-bar"), suggestion.text)
            )

            # Get the updated content of the "products for" section
            updated_content = products_for_section.text

            # Check if the content has changed
            if updated_content != initial_content:
                hovered_suggestions.append(suggestion)

            # Reset the initial content to the updated content for the next iteration
            initial_content = updated_content

        return hovered_suggestions

    def go_to_third_product(self):
        third_product = self.driver.find_elements(By.CSS_SELECTOR, ".sku-title > h4 > a")[2]
        third_product.click()

    def check_price_text_size(self):
        price_element = self.driver.find_element(By.CSS_SELECTOR, ".priceView-hero-price span")
        price_text_size = price_element.value_of_css_property("font-size")
        assert price_text_size == "30px", f"Price text size is not 30px, but {price_text_size}"

    def check_sections(self):
        sections = ["Features", "Specifications", "Questions & Answers"]
        for section in sections:
            section_element = self.driver.find_element(By.XPATH, f"//button[text()='{section}']")
            section_element.click()
            details = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".shop-container"))
            )
            assert details.is_displayed(), f"{section} details not displayed"
