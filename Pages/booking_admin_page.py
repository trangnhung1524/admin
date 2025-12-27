from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class BookingAdminPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators cho trang Danh sách Booking
        self.input_booking_id = (By.NAME, "booking_id")
        self.select_booking_status = (By.ID, "booking_status")
        self.btn_search = (By.ID, "search")
        self.btn_back_main = (By.CSS_SELECTOR, "a.btn-warning") # Nút Back màu vàng
        self.table_rows = (By.CSS_SELECTOR, "table tbody tr")
        self.btn_edit = (By.XPATH, "//a[contains(.,'Edit')]")
        self.btn_invoice = (By.XPATH, "//a[contains(.,'Invoice')]")
        self.pagination_next = (By.XPATH, "//a[contains(text(),'2')]")

        # Locators cho trang Edit Booking
        self.edit_booking_status = (By.NAME, "booking_status")
        self.edit_payment_status = (By.NAME, "payment_status")
        self.btn_submit = (By.ID, "submit")
        self.field_booking_id_readonly = (By.NAME, "booking_id")

    def navigate_to_bookings(self):
        self.driver.find_element(By.XPATH, "//a[contains(.,'Bookings')]").click()

    def search_by_id(self, b_id):
        self.driver.find_element(*self.input_booking_id).clear()
        self.driver.find_element(*self.input_booking_id).send_keys(b_id)
        self.driver.find_element(*self.btn_search).click()

    def filter_status(self, status):
        select = Select(self.driver.find_element(*self.select_booking_status))
        select.select_by_visible_text(status)
        self.driver.find_element(*self.btn_search).click()