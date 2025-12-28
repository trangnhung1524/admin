from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        # Locators
        self.txt_email = (By.NAME, "email")
        self.txt_password = (By.NAME, "password")
        self.btn_login = (By.XPATH, "//button[@type='submit']")
        self.msg_error = (By.XPATH, "//*[contains(text(),'Invalid Login')]")

    def open_page(self):
        self.driver.get("https://phptravels.net/admin/login")

    def enter_email(self, email):
        el = self.wait.until(EC.visibility_of_element_located(self.txt_email))
        el.clear()
        if email: # Chỉ gửi keys nếu email không rỗng
            el.send_keys(email)

    def enter_password(self, password):
        # Sử dụng wait thay vì find_element trực tiếp để ổn định hơn
        el = self.wait.until(EC.visibility_of_element_located(self.txt_password))
        el.clear()
        if password:
            el.send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_login)).click()
        # Xử lý Alert HTML5 hoặc JS Alert nếu có
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except:
            pass

    # Hàm tổng hợp để gọi trong các test case cho ngắn gọn
    def login_action(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        try:
            error_el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.msg_error)
            )
            return error_el.text.strip()
        except Exception as e:
            print("Không bắt được error message:", e)
            return ""