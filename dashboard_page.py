from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # 6 cards thống kê (đúng structure PHPTravels)
        self.cards = (By.CSS_SELECTOR, ".card-body")

        # Widgets
        self.chart_countries = (By.XPATH, "//*[contains(text(),'Most Visited Countries')]")
        self.widget_cancellation = (By.XPATH, "//*[contains(text(),'Booking Cancellation')]")

    def wait_dashboard_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.cards))

    def get_cards(self):
        self.wait_dashboard_loaded()
        return self.driver.find_elements(*self.cards)

    def is_countries_chart_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.chart_countries)
        ).is_displayed()

    def is_cancellation_widget_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.widget_cancellation)
        ).is_displayed()
