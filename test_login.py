import time

import pytest
from selenium import webdriver
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_full_flow(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login = LoginPage(driver)
    login.login("Admin", "admin123")
    assert login.is_dashboard_displayed(), "Login failed."

    employees = [("Divya", "Patel"), ("John", "Doe"), ("Smith", "Singh")]
    for first, last in employees:
        login.navigate_to_pim()
        login.add_employee(first, last)
        time.sleep(2)

    login.navigate_to_pim()
    login.go_to_employee_list()
    for first, last in employees:
        assert login.verify_employee(f"{first} {last}"), f"{first} {last} not found!"

    login.logout()