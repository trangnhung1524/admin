import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Pages.users_admin_page import UsersAdminPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(7)
    # Login giả định
    driver.get("https://phptravels.net/api/admin")
    yield driver
    driver.quit()

class TestUsersManagement:

    # --- NHÓM 1: ALL USERS (01-08) ---
    def test_tc_user_01_load(self, driver):
        assert "Users" in driver.title
        assert driver.find_element(*UsersAdminPage.BTN_ADD).is_displayed()

    def test_tc_user_02_add_btn(self, driver):
        driver.find_element(*UsersAdminPage.BTN_ADD).click()
        assert "Add User" in driver.page_source

    def test_tc_user_03_edit_btn(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        assert driver.find_element(*UsersAdminPage.BTN_UPDATE).is_displayed()

    def test_tc_user_04_del_cancel(self, driver):
        page = UsersAdminPage(driver)
        page.delete_first_user(confirm=False)
        assert driver.find_element(*UsersAdminPage.TABLE_ROWS).is_displayed()

    def test_tc_user_05_del_ok(self, driver):
        page = UsersAdminPage(driver)
        page.delete_first_user(confirm=True)
        assert "deleted" in driver.page_source.lower()

    def test_tc_user_06_toggle(self, driver):
        toggle = driver.find_element(*UsersAdminPage.TOGGLE_STATUS)
        before = toggle.is_selected()
        toggle.click()
        assert toggle.is_selected() != before

    def test_tc_user_07_submenu(self, driver):
        driver.get("https://phptravels.net/api/admin/accounts/customers/")
        assert "Customers" in driver.page_source

    def test_tc_user_08_pagination(self, driver):
        sel = Select(driver.find_element(*UsersAdminPage.DROPDOWN_PAGINATION))
        sel.select_by_value("50")
        assert "50" in driver.find_element(*UsersAdminPage.PAGINATION_50).get_attribute("selected")

    # --- NHÓM 2: ADD USER (01-08) ---
    def test_tc_add_01_success(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "Test", "auto@test.com", "123456", "Customer")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "successfully" in driver.page_source

    def test_tc_add_02_return(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        driver.find_element(*UsersAdminPage.BTN_RETURN).click()
        assert "All Users" in driver.page_source

    def test_tc_add_03_empty(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert driver.find_element(*UsersAdminPage.INP_FNAME).get_attribute("validationMessage") != ""

    def test_tc_add_04_no_fname(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("", "Test", "a@b.com", "123")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "fill out this field" in driver.find_element(*UsersAdminPage.INP_FNAME).get_attribute("validationMessage").lower()

    def test_tc_add_05_no_lname(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "", "a@b.com", "123")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert len(driver.find_element(*UsersAdminPage.INP_LNAME).get_attribute("validationMessage")) > 0

    def test_tc_add_06_wrong_email(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "Test", "invalid-email", "123")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "@" in driver.find_element(*UsersAdminPage.INP_EMAIL).get_attribute("validationMessage")

    def test_tc_add_07_dup_email(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "Test", "admin@phptravels.com", "123", "Customer")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "exists" in driver.page_source.lower()

    def test_tc_add_08_no_type(self, driver):
        page = UsersAdminPage(driver)
        page.go_to_add_user()
        page.fill_form("Auto", "Test", "new@test.com", "123")
        driver.find_element(*UsersAdminPage.BTN_SAVE).click()
        assert "User Type" in driver.page_source

    # --- NHÓM 3: EDIT USER (01-08) ---
    def test_tc_edit_01_update(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        f = driver.find_element(*UsersAdminPage.INP_FNAME)
        f.clear(); f.send_keys("Updated")
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert "successfully" in driver.page_source

    def test_tc_edit_02_toggle(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        driver.find_element(*UsersAdminPage.TOGGLE_STATUS).click()
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert "successfully" in driver.page_source

    def test_tc_edit_03_role(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        Select(driver.find_element(*UsersAdminPage.SEL_TYPE)).select_by_visible_text("Agent")
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert "successfully" in driver.page_source

    def test_tc_edit_04_pass(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        driver.find_element(*UsersAdminPage.INP_PASS).send_keys("New123")
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert "successfully" in driver.page_source

    def test_tc_edit_05_empty_pass(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        driver.find_element(*UsersAdminPage.INP_PASS).clear()
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert "successfully" in driver.page_source

    def test_tc_edit_06_no_fname(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        f = driver.find_element(*UsersAdminPage.INP_FNAME); f.clear()
        driver.find_element(*UsersAdminPage.BTN_UPDATE).click()
        assert len(f.get_attribute("validationMessage")) > 0

    def test_tc_edit_07_readonly(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        curr = driver.find_element(*UsersAdminPage.SEL_CURRENCY)
        assert not curr.is_enabled() or curr.get_attribute("readonly") == "true"

    def test_tc_edit_08_trans(self, driver):
        driver.find_element(*UsersAdminPage.BTN_EDIT).click()
        driver.find_element(*UsersAdminPage.BTN_ADD_TRANSACTION).click()
        assert driver.find_element(By.ID, "add_transaction_modal").is_displayed()