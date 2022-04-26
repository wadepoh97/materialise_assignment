
import pytest
import datetime
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from py.xml import html

@pytest.fixture(scope='function')
def driver():
    chromeOptions = Options()
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
    yield browser
    browser.close()
    browser.quit()

# Report config
def pytest_configure(config):
    config._metadata = None

def pytest_html_report_title(report):
    report.title = "Login Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("This is custom summary")])

def pytest_html_results_table_header(cells):
    # removing old table headers
    del cells[1]
    # adding new headers
    cells.insert(0, html.th('Time', class_='sortable time', col='time'))
    cells.insert(1, html.th('Tag'))
    cells.insert(2, html.th('Testcase'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    del cells[1]
    cells.insert(0, html.td(datetime.datetime.now(), class_='col-time'))
    cells.insert(1, html.td(report.tag))
    cells.insert(2, html.td(report.testcase))
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    # this is the output that is seen end of test case
    report = outcome.get_result()
    # taking doc string of the string
    testcase = str(item.function.__doc__)
    # name of the functton
    c = str(item.function.__name__)[5:]
    
    report.testcase = f"{c} [{testcase}]"
    report.tag = re.split(r"\[|\]", report.nodeid)[-2]