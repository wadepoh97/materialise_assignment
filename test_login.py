
import pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from utilities import inject_test_data

test_data = inject_test_data(file="data.json")

@pytest.mark.parametrize("account", test_data.test_login)
def test_login(driver, account):
    driver.get(account.url)
    driver.find_element(By.ID, 'Email').clear()
    driver.find_element(By.ID, 'Password').clear()

    driver.find_element(By.ID, 'Email').send_keys(account.email)
    driver.find_element(By.ID, 'Password').send_keys(account.password)
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()

    # if can find logout btn & .Nop.Authentication cookies = valid
    try:
        auth = driver.get_cookie('.Nop.Authentication')
        if auth is None: raise NoSuchElementException 
        logout = driver.find_element(By.XPATH, "//a[@href='/logout']")
        logout.click()
    except NoSuchElementException:
        err_msg = driver.find_element(By.CLASS_NAME, "message-error")
        if 'Login was unsuccessful' in err_msg.text: raise Exception('Invalid Credentials')
        ## assuming the all email format in test data are correct
        ## if cannot find the message-error will raise here