import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from login_admin_page import LoginAdminPage
from booking_admin_page import BookingAdminPage


class TestBookingAdmin:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        self.login_p = LoginAdminPage(driver)
        self.book_p = BookingAdminPage(driver)

        # ===== LOGIN =====
        self.login_p.open_page()
        self.login_p.login_action(
            "admin@phptravels.com",
            "demoadmin"
        )

        # ===== GO TO BOOKINGS =====
        self.book_p.navigate_to_bookings()
        self.book_p.wait_table_loaded()

    # ================= LIST PAGE =================

    def test_tc_book_01_load_page(self):
        assert "bookings" in self.driver.page_source.lower()
        assert self.driver.find_element(*self.book_p.btn_search).is_displayed()

    def test_tc_book_02_filter_confirmed(self):
        self.book_p.filter_by_status("Confirmed")
        self.book_p.wait_table_loaded()
        assert "confirmed" in self.driver.page_source.lower()

    def test_tc_book_03_search_id_valid(self):
        self.book_p.search_by_id("20251021093642")
        self.book_p.wait_table_loaded()
        assert "20251021093642" in self.driver.page_source

    def test_tc_book_04_search_id_invalid(self):
        self.book_p.search_by_id("999999999")
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        rows = self.driver.find_elements(
            By.CSS_SELECTOR, "table tbody tr"
        )
        assert len(rows) == 0

    def test_tc_book_05_view_invoice(self):
        main_window = self.driver.current_window_handle
        self.wait.until(
            EC.element_to_be_clickable(self.book_p.btn_invoice)
        ).click()
        self.wait.until(lambda d: len(d.window_handles) > 1)
        for window in self.driver.window_handles:
            if window != main_window:
                self.driver.switch_to.window(window)
                break
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Booking Reference')]")
            )
        )
        assert "booking reference" in self.driver.page_source.lower()
        assert "phptravels" in self.driver.page_source.lower()
        self.driver.close()
        self.driver.switch_to.window(main_window)

    def test_tc_book_06_click_edit(self):
        self.book_p.open_edit_page()
        assert "edit" in self.driver.current_url.lower()

    # ================= EDIT PAGE =================

    def test_tc_book_edit_01_status_cancelled(self):
        self.book_p.open_edit_page()
        Select(
            self.driver.find_element(*self.book_p.edit_booking_status)
        ).select_by_visible_text("Cancelled")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "bookings" in self.driver.current_url.lower()

    def test_tc_book_edit_02_payment_paid(self):
        self.book_p.open_edit_page()
        Select(
            self.driver.find_element(*self.book_p.edit_payment_status)
        ).select_by_visible_text("Paid")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "bookings" in self.driver.current_url.lower()

    def test_tc_book_edit_03_update_both(self):
        self.book_p.open_edit_page()
        Select(
            self.driver.find_element(*self.book_p.edit_booking_status)
        ).select_by_visible_text("Confirmed")
        Select(
            self.driver.find_element(*self.book_p.edit_payment_status)
        ).select_by_visible_text("Paid")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "bookings" in self.driver.current_url.lower()

    def test_tc_book_edit_04_back_without_save(self):
        self.book_p.open_edit_page()
        self.driver.find_element(*self.book_p.btn_back).click()
        assert "bookings" in self.driver.current_url.lower()

    def test_tc_book_edit_05_booking_id_displayed(self):
        self.book_p.open_edit_page()
        assert self.driver.find_element(
            *self.book_p.text_booking_id
        ).is_displayed()
