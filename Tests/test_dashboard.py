import pytest
from selenium.webdriver.common.by import By
from Pages.login_admin_page import LoginAdminPage
from Pages.dashboard_page import DashboardPage

class TestDashboardGUI:
    @pytest.fixture(autouse=True)
    def setup_dashboard(self, driver):
        self.driver = driver
        self.login_p = LoginAdminPage(self.driver)
        self.dash_p = DashboardPage(self.driver)
        # Login để vào Dashboard
        self.driver.get("https://phptravels.net/api/admin")
        self.login_p.perform_login("admin@phptravels.com", "demoadmin")

    def test_layout(self):
        """TC-DASH-01: Kiểm tra tải trang và bố cục (6 thẻ, 2 widget)"""
        cards = self.dash_p.get_cards()
        assert len(cards) >= 6, "Không hiển thị đủ 6 thẻ thống kê"
        assert self.dash_p.get_chart_display_status() is True
        assert self.dash_p.get_cancellation_widget_status() is True

    def test_card_data(self):
        """TC-DASH-02: Kiểm tra tên 6 thẻ hiển thị chính xác"""
        expected_names = ["Users", "Pages", "Bookings", "Cancelled Bookings", "Unpaid Bookings", "Pending Transactions"]
        page_content = self.driver.page_source
        for name in expected_names:
            assert name in page_content, f"Thiếu thẻ thống kê: {name}"

    def test_click_behavior(self):
        """TC-DASH-03: Kiểm tra hành vi Hover"""
        first_card = self.dash_p.get_cards()[0]
        # Kiểm tra con trỏ không phải 'pointer' (bàn tay) mà là 'default' (mũi tên)
        cursor_style = first_card.value_of_css_property("cursor")
        assert cursor_style == "auto" or cursor_style == "default"

    def test_countries_chart(self):
        """TC-DASH-04: Kiểm tra hiển thị Biểu đồ quốc gia"""
        assert self.dash_p.get_chart_display_status() is True
        # Kiểm tra sự hiện diện của canvas biểu đồ
        chart_canvas = self.driver.find_elements(By.TAG_NAME, "canvas")
        assert len(chart_canvas) > 0, "Biểu đồ không tải được dữ liệu"

    def test_cancellation_widget(self):
        """TC-DASH-05: Kiểm tra widget Hủy phòng"""
        assert self.dash_p.get_cancellation_widget_status() is True
        # Kiểm tra nội dung mặc định khi không có dữ liệu
        msg = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No Booking')]").text
        assert "No Booking Cancellation Request" in msg