import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from configs.environment import BASE_URL

@pytest.fixture(scope="function")
def driver():
    """Setup WebDriver fixture with teardown."""
    service = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service)
    _driver.get(BASE_URL)
    yield _driver
    _driver.quit()
