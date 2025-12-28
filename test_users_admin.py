import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from login_admin_page import LoginAdminPage
from users_admin_page import UsersAdminPage

@pytest.fixture(scope="class")
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("driver")
class TestUsersAdmin:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.wait = WebDriverWait(self.driver, 15)
        self.login_p = LoginAdminPage(self.driver)
        self.user_p = UsersAdminPage(self.driver)

        # LOGIN
        self.login_p.open_page()
        self.login_p.login_action("admin@phptravels.com", "demoadmin")

        # VÀO USERS
        self.user_p.navigate_to_users()
        self.user_p.wait_table_loaded()

    # ================= TC01 =================
    def test_tc_user_01_load(self):
        """Test giao diện trang Users"""
        assert self.driver.find_element(*self.user_p.btn_add).is_displayed()
        assert self.driver.find_element(*self.user_p.table_rows).is_displayed()

    # ================= TC02 =================
    def test_tc_user_02_click_add(self):
        """Click Add → sang trang Add User"""
        self.user_p.open_add_page()
        assert self.driver.find_element(*self.user_p.add_title).is_displayed()

    # ================= TC03 =================
    def test_tc_user_03_click_edit(self):
        """Click Edit → sang trang Edit User"""
        self.user_p.open_edit_page()
        assert self.driver.find_element(*self.user_p.edit_title).is_displayed()

    def test_tc_user_04_delete_cancel(self):
        self.user_p.delete_first_user(confirm=False)
        self.user_p.wait_table_loaded()

    def test_tc_user_05_delete_ok(self):
        self.user_p.delete_first_user(confirm=True)
        self.user_p.wait_table_loaded()

    def test_tc_user_06_toggle(self):
        t = self.driver.find_element(*self.user_p.toggle_status)
        before = t.is_selected()
        t.click()
        assert t.is_selected() != before

    def test_tc_user_07_filter_customer(self):
        self.driver.find_element(*self.user_p.submenu_customer).click()
        assert "customer" in self.driver.page_source.lower()

    def test_tc_user_08_pagination(self):
        self.driver.find_element(*self.user_p.pagination_50).click()
        self.user_p.wait_table_loaded()

    # ===== ADD =====
    def test_tc_add_01_success(self, driver: WebDriver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "Test", "auto123@test.com", "123456", "Customer")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "users" in driver.current_url.lower()

    def test_tc_user_add_02_return(self):
        self.user_p.open_add_page()
        self.driver.find_element(*self.user_p.btn_return).click()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_add_03_empty(self):
        self.user_p.open_add_page()
        self.user_p.submit()
        assert self.driver.find_element(
            *self.user_p.inp_fname
        ).get_attribute("validationMessage") != ""

    def test_tc_user_add_04_no_fname(self):
        self.user_p.open_add_page()
        self.user_p.fill_user_form(lname="User", email="a@b.com", password="123")
        self.user_p.submit()
        assert self.driver.find_element(
            *self.user_p.inp_fname
        ).get_attribute("validationMessage") != ""

    def test_tc_user_add_05_no_lname(self):
        self.user_p.open_add_page()
        self.user_p.fill_user_form(fname="Test", email="a@b.com", password="123")
        self.user_p.submit()
        assert self.driver.find_element(
            *self.user_p.inp_lname
        ).get_attribute("validationMessage") != ""

    def test_tc_user_add_06_invalid_email(self):
        self.user_p.open_add_page()
        self.user_p.fill_user_form(
            "Test", "User", "abcde", "123"
        )
        self.user_p.submit()
        assert self.driver.find_element(
            *self.user_p.inp_email
        ).get_attribute("validationMessage") != ""

    def test_tc_user_add_07_dup_email(self):
        self.user_p.open_add_page()
        self.user_p.fill_user_form(
            "Test", "User", "admin@phptravels.com", "123", "Customer"
        )
        self.user_p.submit()
        assert "add" in self.driver.current_url.lower()

    def test_tc_user_add_08_no_type(self):
        self.user_p.open_add_page()
        self.user_p.fill_user_form(
            "Test", "User", "x@y.com", "123"
        )
        self.user_p.submit()
        assert "add" in self.driver.current_url.lower()

    # ===== EDIT =====
    def test_tc_user_edit_01_update(self):
        self.user_p.open_edit_page()
        f = self.driver.find_element(*self.user_p.inp_fname)
        f.clear()
        f.send_keys("Updated")
        self.user_p.submit()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_edit_02_toggle(self):
        self.user_p.open_edit_page()
        self.driver.find_element(*self.user_p.toggle_status).click()
        self.user_p.submit()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_edit_03_role(self):
        self.user_p.open_edit_page()
        Select(
            self.driver.find_element(*self.user_p.sel_type)
        ).select_by_index(1)
        self.user_p.submit()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_edit_04_password(self):
        self.user_p.open_edit_page()
        self.driver.find_element(
            *self.user_p.inp_password
        ).send_keys("NewPass123")
        self.user_p.submit()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_edit_05_empty_password(self):
        self.user_p.open_edit_page()
        self.user_p.submit()
        assert "users" in self.driver.current_url.lower()

    def test_tc_user_edit_06_no_fname(self):
        self.user_p.open_edit_page()
        f = self.driver.find_element(*self.user_p.inp_fname)
        f.clear()
        self.user_p.submit()
        assert f.get_attribute("validationMessage") != ""

    def test_tc_user_edit_07_readonly(self):
        self.user_p.open_edit_page()
        assert not self.driver.find_element(
            *self.user_p.sel_currency
        ).is_enabled()

    def test_tc_user_edit_08_transaction(self):
        self.user_p.open_edit_page()
        self.driver.find_element(
            *self.user_p.btn_add_transaction
        ).click()
        assert self.driver.find_element(
            *self.user_p.modal_transaction
        ).is_displayed()
