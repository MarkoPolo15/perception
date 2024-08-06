import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.home_page import HomePage
from src.utilities.credentials import load_credentials
from configs.environment import BASE_URL

def test_search_results(home_page):
    results = home_page.check_search_results()
    assert len(results) > 0, "No search suggestions found"
    print(f"Found {len(results)} suggestions: {[result.text for result in results]}")
    return results

def test_hover_over_suggestions(home_page):
    results = home_page.check_search_results()
    assert len(results) > 0, "No search suggestions found"
    initial_right_side_content = home_page.get_right_side_content()
    print(f"Initial right side content: {initial_right_side_content}")

    # Start from the second result
    for i, result in enumerate(results[1:], start=2):
        home_page.hover_over_element(result)
        current_right_side_content = home_page.get_right_side_content()
        print(f"Hovered over element {i} with text: {result.text}")
        print(f"Current right side content: {current_right_side_content}")

        if current_right_side_content == initial_right_side_content:
            print(f"Right side content did not change for {result.text}")
        else:
            print(f"Right side content changed for {result.text}")

        assert current_right_side_content != initial_right_side_content, f"Right side content did not change for {result.text}"
        initial_right_side_content = current_right_side_content
        break

def test_check_price_text_size(home_page):
    home_page.go_to_third_product()
    price_text_size, price_text = home_page.get_price_text_size()
    assert price_text_size == "30px", f"Price text size is not 30px, but {price_text_size}"
    assert price_text, "Price text is empty"

def test_check_specifications(home_page):
    home_page.go_to_third_product()
    spec_content = home_page.get_specifications()
    assert spec_content, "Specifications content is empty"

def test_check_features(home_page):
    home_page.go_to_third_product()
    feature_text = home_page.get_features()
    assert feature_text, "Features text is empty"

 