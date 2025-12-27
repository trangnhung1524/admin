from selenium.webdriver.common.by import By

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        # 6 thẻ thống kê
        self.stat_cards = (By.CSS_SELECTOR, ".row .card") # Selector chung cho các thẻ
        self.card_titles = (By.CSS_SELECTOR, ".card .title") # Giả định class title dựa trên UI
        
        # 2 Widgets bên dưới
        self.chart_countries = (By.XPATH, "//div[contains(., '10 Most Visited Countries')]")
        self.widget_cancellation = (By.XPATH, "//div[contains(., 'Booking Cancellation Request')]")
        self.no_request_msg = (By.XPATH, "//div[contains(text(), 'No Booking Cancellation Request')]")

    def get_cards(self):
        return self.driver.find_elements(By.XPATH, "//div[@class='card-body']")

    def get_chart_display_status(self):
        return self.driver.find_element(*self.chart_countries).is_displayed()

    def get_cancellation_widget_status(self):
        return self.driver.find_element(*self.widget_cancellation).is_displayed()