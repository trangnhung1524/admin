from selenium.webdriver.common.by import By

class LoginAdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.txt_email = (By.NAME, "email")
        self.txt_password = (By.NAME, "password")
        self.btn_login = (By.XPATH, "//button[@type='submit']")
        self.msg_error = (By.CSS_SELECTOR, ".alert-danger")

    def open_page(self):
        self.driver.get("https://phptravels.net/api/admin")

    def enter_email(self, email):
        self.driver.find_element(*self.txt_email).clear()
        self.driver.find_element(*self.txt_email).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.txt_password).clear()
        self.driver.find_element(*self.txt_password).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.btn_login).click()

    def get_error_message(self):
        return self.driver.find_element(*self.msg_error).text