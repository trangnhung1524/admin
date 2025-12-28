from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class BookingAdminPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # ================= LIST PAGE =================
        self.menu_bookings = (By.XPATH, "//a[contains(.,'Bookings')]")

        self.input_booking_id = (By.NAME, "booking_id")
        self.select_filter_booking_status = (
            By.XPATH, "//select[@name='booking_status']"
        )
        self.btn_search = (By.XPATH, "//button[contains(text(),'Search')]")

        self.table_rows = (By.CSS_SELECTOR, "table tbody tr")
        self.btn_edit = (By.XPATH, "//table//a[contains(text(),'Edit')]")
        self.btn_invoice = (By.XPATH, "//table//a[contains(text(),'Invoice')]")

        # ================= EDIT PAGE =================
        self.edit_booking_status = (
            By.XPATH, "//form//select[@name='booking_status']"
        )
        self.edit_payment_status = (
            By.XPATH, "//form//select[@name='payment_status']"
        )
        self.btn_submit = (By.XPATH, "//button[contains(text(),'Submit')]")
        self.btn_back = (By.XPATH, "//a[contains(text(),'Back')]")

        # Booking ID text (NOT input field)
        self.text_booking_id = (
            By.XPATH, "//*[contains(text(),'Booking ID')]"
        )

    # ================= ACTIONS =================

    def navigate_to_bookings(self):
        self.wait.until(
            EC.element_to_be_clickable(self.menu_bookings)
        ).click()

    def wait_table_loaded(self):
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

    def search_by_id(self, booking_id):
        field = self.wait.until(
            EC.visibility_of_element_located(self.input_booking_id)
        )
        field.clear()
        field.send_keys(booking_id)
        self.driver.find_element(*self.btn_search).click()

    def filter_by_status(self, status):
        Select(
            self.wait.until(
                EC.visibility_of_element_located(
                    self.select_filter_booking_status
                )
            )
        ).select_by_visible_text(status)
        self.driver.find_element(*self.btn_search).click()

    def open_edit_page(self):
        self.wait.until(
            EC.element_to_be_clickable(self.btn_edit)
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(self.edit_booking_status)
        )
