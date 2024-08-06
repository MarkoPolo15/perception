import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.login import LogIn
from src.utilities.credentials import load_credentials
from configs.environment import BASE_URL
from src.pages.home_page import HomePage



@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver fixture with teardown."""
    service = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service)
    yield _driver
    _driver.quit()

@pytest.fixture(scope="session")
def login(driver):
    """Login fixture to login once per session."""
    login_page = LogIn(driver)
    login_page.select_country()
    login_page.open_sign_in_menu()
    login_page.click_sign_in()
    credentials = load_credentials()['users'][0]
    login_page.login(credentials['username'], credentials['password'])
    yield

@pytest.fixture(scope="session")
#def home_page(driver, login): remove in case you want to use login 
def home_page(driver):
    home_page = HomePage(driver)
    home_page.navigate_to_home()
    home_page.perform_search("hello kitty")
    return home_page