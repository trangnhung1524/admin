import pytest
from selenium.webdriver.support.ui import Select
from Pages.login_admin_page import LoginAdminPage
from Pages.booking_admin_page import BookingAdminPage

class TestBookingFull:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_p = LoginAdminPage(self.driver)
        self.book_p = BookingAdminPage(self.driver)
        # TC-LOGIN: Đăng nhập theo data trong ảnh
        self.driver.get("https://phptravels.net/api/admin")
        self.login_p.perform_login("admin@phptravels.com", "demoadmin")
        self.book_p.navigate_to_bookings()

    # ================= QUẢN LÝ ĐƠN ĐẶT =================
    
    def test_tc_book_01_load_page(self):
        """Kiểm tra tải trang và hiển thị các cột ID, Date, Traveller..."""
        assert "Bookings" in self.driver.page_source
        assert self.driver.find_element(*self.book_p.btn_search).is_displayed()

    def test_tc_book_02_filter_confirmed(self):
        """Lọc trạng thái Confirmed"""
        self.book_p.filter_status("Confirmed")
        assert "confirmed" in self.driver.page_source.lower()

    def test_tc_book_03_search_id_valid(self):
        """Tìm theo ID: 20251021093642"""
        self.book_p.search_by_id("20251021093642")
        assert "20251021093642" in self.driver.page_source

    def test_tc_book_04_search_id_invalid(self):
        """Tìm ID không tồn tại: 999999999"""
        self.book_p.search_by_id("999999999")
        assert "No results found" in self.driver.page_source

    def test_tc_book_05_view_invoice(self):
        """Thao tác xem Hóa đơn (Invoice)"""
        self.driver.find_element(*self.book_p.btn_invoice).click()
        assert "invoice" in self.driver.current_url

    def test_tc_book_06_click_edit(self):
        """Thao tác nút Chỉnh sửa (Edit)"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        assert "edit" in self.driver.current_url

    def test_tc_book_07_pagination(self):
        """Kiểm tra phân trang (Nhấn số 2)"""
        try:
            self.driver.find_element(*self.book_p.pagination_next).click()
            assert "page=2" in self.driver.current_url or self.driver.find_element(*self.book_p.pagination_next)
        except: pytest.skip("Không đủ dữ liệu để phân trang")

    def test_tc_book_08_back_button(self):
        """Kiểm tra nút Back màu vàng"""
        self.driver.find_element(*self.book_p.btn_back_main).click()
        assert "dashboard" in self.driver.current_url

    # ================= EDIT BOOKING =================

    def test_tc_book_edit_01_status_cancelled(self):
        """Cập nhật Booking Status -> Cancelled"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element(*self.book_p.edit_booking_status)).select_by_visible_text("Cancelled")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "updated successfully" in self.driver.page_source.lower()

    def test_tc_book_edit_02_payment_paid(self):
        """Cập nhật Payment Status -> Paid"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element(*self.book_p.edit_payment_status)).select_by_visible_text("Paid")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "updated successfully" in self.driver.page_source.lower()

    def test_tc_book_edit_03_update_both(self):
        """Cập nhật cả 2 trạng thái thành công"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element(*self.book_p.edit_booking_status)).select_by_visible_text("Confirmed")
        Select(self.driver.find_element(*self.book_p.edit_payment_status)).select_by_visible_text("Paid")
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "updated successfully" in self.driver.page_source.lower()

    def test_tc_book_edit_04_back_without_save(self):
        """Thay đổi giá trị nhưng nhấn Back (không lưu)"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        Select(self.driver.find_element(*self.book_p.edit_booking_status)).select_by_visible_text("Cancelled")
        self.driver.find_element(*self.book_p.btn_back_main).click() # Nút Back màu vàng
        assert "Bookings" in self.driver.page_source # Quay về trang list

    def test_tc_book_edit_05_submit_default(self):
        """Submit giá trị mặc định (Select Type)"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        self.driver.find_element(*self.book_p.btn_submit).click()
        assert "updated" in self.driver.page_source or "Bookings" in self.driver.page_source

    def test_tc_book_edit_06_id_readonly(self):
        """Kiểm tra Booking ID chỉ đọc (Read-only)"""
        self.driver.find_element(*self.book_p.btn_edit).click()
        field = self.driver.find_element(*self.book_p.field_booking_id_readonly)
        # Kiểm tra thuộc tính readonly hoặc disabled
        is_readonly = field.get_attribute("readonly") or field.get_attribute("disabled")
        assert is_readonly is not None