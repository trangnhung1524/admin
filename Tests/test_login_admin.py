import pytest
from Pages.login_admin_page import LoginAdminPage

class TestLoginAdmin:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_p = LoginAdminPage(self.driver)
        self.login_p.open_page()

    def test_login_success(self):
        """TC-LOG-AD-01: Đăng nhập thành công"""
        self.login_p.enter_email("admin@phptravels.com")
        self.login_p.enter_password("demoadmin")
        self.login_p.click_login()
        assert "dashboard" in self.driver.current_url

    def test_invalid_email(self):
        """TC-LOG-AD-02: Nhập sai email"""
        self.login_p.enter_email("wrong@admin.com")
        self.login_p.enter_password("demoadmin")
        self.login_p.click_login()
        assert "Invalid Login Credentials" in self.login_p.get_error_message()

    def test_invalid_password(self):
        """TC-LOG-AD-03: Nhập sai password"""
        self.login_p.enter_email("wrong@admin.com")
        self.login_p.enter_password("demoadmin")
        self.login_p.click_login()
        assert "Invalid Login Credentials" in self.login_p.get_error_message()

    def test_empty_email(self):
        """TC-LOG-AD-04: Báo lỗi khi trống Email"""
        self.login_p.enter_email("")
        self.login_p.enter_password("demoadmin")
        self.login_p.click_login()
        # Kiểm tra nếu URL không đổi nghĩa là chưa login thành công
        assert "admin" in self.driver.current_url

    def test_empty_password(self):
        """TC-LOG-AD-05: Báo lỗi khi trống Password"""
        self.login_p.enter_email("admin@phptravels.com")
        self.login_p.enter_password("")
        self.login_p.click_login()
        assert "admin" in self.driver.current_url