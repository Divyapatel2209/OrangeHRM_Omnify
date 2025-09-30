from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        self.username_input = (By.XPATH, "//input[@placeholder='Username']")
        self.password_input = (By.XPATH, "//input[@placeholder='Password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")
        self.pim_menu = (By.XPATH, "//span[text()='PIM']")
        self.add_employee_button = (By.XPATH, "//button[normalize-space()='Add']")
        self.first_name_input = (By.NAME, "firstName")
        self.last_name_input = (By.NAME, "lastName")
        self.save_button = (By.XPATH, "//button[@type='submit']")
        self.employee_list_tab = (By.XPATH, "//span[text()='Employee List']/ancestor::a")
        self.employee_names = (By.XPATH, "//div[@class='oxd-table-card']//div[2]")
        self.profile_dropdown = (By.CLASS_NAME, "oxd-userdropdown-name")
        self.logout_button = (By.XPATH, "//a[text()='Logout']")

    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_input)
        ).send_keys(username)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_input)
        ).send_keys(password)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def is_dashboard_displayed(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.dashboard_header)
        ).is_displayed()

    def navigate_to_pim(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.pim_menu)
        )
        pim = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.pim_menu)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", pim)
        time.sleep(1)
        pim.click()

    def add_employee(self, first_name, last_name):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_employee_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        self.driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.first_name_input)
        ).send_keys(first_name)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.last_name_input)
        ).send_keys(last_name)

        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
        self.driver.execute_script("arguments[0].click();", save_btn)
        time.sleep(2)

    def go_to_employee_list(self):
        pim_menu = (By.XPATH, "//span[text()='PIM']")
        first_name_input = (By.XPATH, "(//input[@placeholder='Type for hints...'])[1]")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(pim_menu)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(first_name_input)
        )


    def verify_employee(self, full_name):
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Wait for the Employee List search inputs
        first_name_input = (By.XPATH, "(//input[@placeholder='Type for hints...'])[1]")

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(first_name_input)
        )

        # Split first and last name
        try:
            first = full_name.split(" ", 1)
        except ValueError:
            first  = full_name, ""
        # Enter in the filter form
        first_box = self.driver.find_element(*first_name_input)
        first_box.clear()
        first_box.send_keys(first)



        # Click the search button (rightmost orange button)
        search_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        search_btn.click()
        time.sleep(2)  # Let the table update

        # Now look for the employee name in the table (third cell in the row)
        try:
            name_cell = self.driver.find_element(
                By.XPATH, f"//div[@class='oxd-table-body']//div[@role='row']/div[3][div[text()='{full_name}']]"
            )
            print(f"{full_name}: Name Verified ✅")
            return True
        except Exception:
            print(f"{full_name}: Not Found ❌")
            return False

    def logout(self):
        profile = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.profile_dropdown)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", profile)
        profile.click()

        logout_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.logout_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
        logout_btn.click()