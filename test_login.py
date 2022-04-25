
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup():
    global driver
    chromeOptions = Options()
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
    yield
    driver.close()
    driver.quit()

@pytest.mark.parametrize("username,password,expected", [
    ("admin@yourstore.com","admin",True),
    ("admin@yourstore.com","adm",False), 
    ("adm@yourstore.com","admin",False),
    ("adm@yourstore.com","adm",False)])
def test_login(setup, username, password, expected):
    driver.get('https://admin-demo.nopcommerce.com')
    driver.find_element(By.ID, 'Email').clear()
    driver.find_element(By.ID, 'Password').clear()
    driver.find_element(By.ID, 'Email').send_keys(username)
    driver.find_element(By.ID, 'Password').send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()

    logout = driver.find_element(By.XPATH, "//a[@href='/logout']")
    logout.click()