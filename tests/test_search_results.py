import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.home_page import HomePage
from src.utilities.credentials import load_credentials
from configs.environment import BASE_URL

def test_product_search(driver):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    
    home_page.select_country()
    #home_page.open_sign_in_menu()
    #home_page.click_sign_in()
    
    credentials = load_credentials()['users'][0]
    #home_page.login(credentials['username'], credentials['password'])
    
    home_page.perform_search("hello kitty")
    home_page.check_search_results()
    
    # Hover over each suggestion and verify the "Products for" section changes
    suggestions = home_page.driver.find_elements(By.CSS_SELECTOR, '.suggestions-dropdown .suggestions-box ul li')
    assert len(suggestions) > 0, "No search suggestions found"

    products_for_section = home_page.driver.find_element(By.CSS_SELECTOR, ".gh-search-nav-bar")
    initial_text = products_for_section.text
    
    for suggestion in suggestions:
        action = ActionChains(home_page.driver)
        action.move_to_element(suggestion).perform()
        time.sleep(1)  # Wait for the hover effect to take place
        current_text = products_for_section.text
        assert current_text != initial_text, f"'Products for' section did not change for {suggestion.text}"
        initial_text = current_text
    
    # Go to the third product in the list
    home_page.go_to_third_product()
    
    # Check if there's a price and the text size is 30px
    price_element = home_page.driver.find_element(By.CSS_SELECTOR, ".priceView-hero-price span")
    price_text_size = price_element.value_of_css_property("font-size")
    assert price_text_size == "30px", f"Price text size is not 30px, but {price_text_size}"
    
    # Check sections
    sections = ["Features", "Specifications", "Questions & Answers"]
    for section in sections:
        section_element = home_page.driver.find_element(By.XPATH, f"//button[text()='{section}']")
        section_element.click()
        details = WebDriverWait(home_page.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".shop-container"))
        )
        assert details.is_displayed(), f"{section} details not displayed"
