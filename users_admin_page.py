from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class UsersAdminPage:

    # ================= LIST PAGE =================
    btn_add = (By.XPATH, "//a[contains(@href,'users/add')]")
    btn_edit_first = (By.XPATH, "(//a[contains(@href,'users/edit')])[1]")
    btn_delete_first = (By.XPATH, "(//a[contains(@onclick,'delete')])[1]")
    toggle_status_first = (By.XPATH, "(//input[@type='checkbox'])[1]")

    table_body = (By.CSS_SELECTOR, "table tbody")
    table_rows = (By.CSS_SELECTOR, "table tbody tr")

    submenu_customer = (By.XPATH, "//a[contains(@href,'accounts/customers')]")
    pagination_50 = (By.XPATH, "//a[text()='50']")

    # ================= ADD PAGE =================
    add_title = (By.XPATH, "//h3[contains(text(),'Add User')]")

    # ================= EDIT PAGE =================
    edit_title = (By.XPATH, "//h3[contains(text(),'Edit User')]")

    inp_fname = (By.NAME, "fname")
    inp_lname = (By.NAME, "lname")
    inp_email = (By.NAME, "email")
    inp_password = (By.NAME, "password")
    sel_type = (By.NAME, "type")
    sel_currency = (By.NAME, "currency")
    inp_balance = (By.NAME, "balance")

    btn_submit = (By.ID, "submit")
    btn_return = (By.XPATH, "//a[contains(text(),'Return')]")

    # ================= TRANSACTION =================
    btn_add_transaction = (By.XPATH, "//button[contains(text(),'+ Add')]")
    modal_transaction = (By.ID, "add_transaction_modal")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ================= NAVIGATION =================
    def navigate_to_users(self):
        self.driver.get("https://phptravels.net/admin/users")

    def wait_table_loaded(self):
        self.wait.until(
            EC.presence_of_element_located(self.table_body)
        )

    # ================= ACTIONS =================
    def open_add_page(self):
        self.wait.until(
            EC.element_to_be_clickable(self.btn_add)
        ).click()

        # đảm bảo đã vào Add User
        self.wait.until(
            EC.visibility_of_element_located(self.add_title)
        )

    def open_edit_page(self):
        self.wait_table_loaded()

        self.wait.until(
            EC.element_to_be_clickable(self.btn_edit_first)
        ).click()

        # đảm bảo đã vào Edit User
        self.wait.until(
            EC.visibility_of_element_located(self.edit_title)
        )

    def fill_user_form(self, fname="", lname="", email="", password="", utype=None):
        if fname:
            f = self.driver.find_element(*self.inp_fname)
            f.clear()
            f.send_keys(fname)

        if lname:
            l = self.driver.find_element(*self.inp_lname)
            l.clear()
            l.send_keys(lname)

        if email:
            e = self.driver.find_element(*self.inp_email)
            e.clear()
            e.send_keys(email)

        if password:
            p = self.driver.find_element(*self.inp_password)
            p.clear()
            p.send_keys(password)

        if utype:
            Select(
                self.driver.find_element(*self.sel_type)
            ).select_by_visible_text(utype)

    def submit(self):
        self.driver.find_element(*self.btn_submit).click()

    def delete_first_user(self, confirm=True):
        self.wait.until(
            EC.element_to_be_clickable(self.btn_delete_first)
        ).click()

        alert = self.wait.until(EC.alert_is_present())
        alert.accept() if confirm else alert.dismiss()
    USERS_URL = "https://phptravels.net/api/admin/accounts/users/"

    btn_add = (By.CSS_SELECTOR, "a.btn-success")
    btn_edit = (By.CSS_SELECTOR, "a.btn-primary")
    table_rows = (By.CSS_SELECTOR, "table tbody tr")

    add_title = (By.XPATH, "//h3[contains(text(),'Add')]")
    edit_title = (By.XPATH, "//h3[contains(text(),'Edit')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def navigate_to_users(self):
        self.driver.get(self.USERS_URL)

    def wait_table_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.table_rows))

    def open_add_page(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_add)).click()

    def open_edit_page(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_edit)).click()