import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from login_admin_page import LoginAdminPage
from dashboard_page import DashboardPage

class TestDashboardGUI:

    @pytest.fixture(autouse=True)
    def setup_dashboard(self, driver: WebDriver):
        self.driver = driver
        self.login_p = LoginAdminPage(driver)
        self.dash_p = DashboardPage(driver)

        # Login chuẩn
        self.login_p.open_page()
        self.login_p.login_action("admin@phptravels.com", "demoadmin")

        # Chờ dashboard load
        self.dash_p.wait_dashboard_loaded()

    def test_layout(self):
        """TC-DASH-01: Kiểm tra bố cục"""
        cards = self.dash_p.get_cards()
        assert len(cards) >= 6, f"Chỉ tìm thấy {len(cards)} cards"
        assert self.dash_p.is_countries_chart_displayed()
        assert self.dash_p.is_cancellation_widget_displayed()

    def test_card_data(self):
        """TC-DASH-02: Kiểm tra tên các thẻ"""
        expected_names = [
            "Users",
            "Pages",
            "Bookings",
            "Cancelled Bookings",
            "Unpaid Bookings",
            "Pending Transactions"
        ]

        page_text = self.driver.page_source
        for name in expected_names:
            assert name in page_text, f"Thiếu card: {name}"

    

    def test_click_behavior(self):
        """TC-DASH-03: Click card → chuyển sang trang khác"""
        cards = self.dash_p.get_cards()
        assert len(cards) > 0, "Không tìm thấy card nào trên Dashboard"
        first_card = cards[0]
        current_url = self.driver.current_url
        first_card.click()
        # Chờ URL thay đổi
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url != current_url
        )
        new_url = self.driver.current_url
        assert new_url != current_url, "Click card nhưng không chuyển trang"

    def test_countries_chart(self):
        """TC-DASH-04: Biểu đồ quốc gia"""
        assert self.dash_p.is_countries_chart_displayed()

        canvases = self.driver.find_elements(By.TAG_NAME, "canvas")
        assert len(canvases) > 0, "Không tìm thấy canvas biểu đồ"

    def test_cancellation_widget(self):
        """TC-DASH-05: Widget hủy booking"""
        assert self.dash_p.is_cancellation_widget_displayed()

        page_text = self.driver.page_source
        assert (
            "No Booking Cancellation Request" in page_text
            or "Cancellation" in page_text
        )
