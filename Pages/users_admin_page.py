from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class UsersAdminPage:
    BTN_ADD = (By.CSS_SELECTOR, "a.btn-success")
    INP_FNAME = (By.NAME, "fname")
    INP_LNAME = (By.NAME, "lname")
    INP_EMAIL = (By.NAME, "email")
    INP_PASS = (By.NAME, "password")
    SEL_TYPE = (By.NAME, "type")
    BTN_SAVE = (By.ID, "save")
    BTN_UPDATE = (By.ID, "update")
    BTN_EDIT = (By.CSS_SELECTOR, ".btn-primary i.fa-edit")
    BTN_DELETE = (By.CSS_SELECTOR, ".btn-danger i.fa-trash")

    def __init__(self, driver):
        self.driver = driver

    def go_to_add_user(self):
        self.driver.find_element(*self.BTN_ADD).click()

    def fill_form(self, fname="", lname="", email="", password="", utype=None):
        if fname: self.driver.find_element(*self.INP_FNAME).send_keys(fname)
        if lname: self.driver.find_element(*self.INP_LNAME).send_keys(lname)
        if email: self.driver.find_element(*self.INP_EMAIL).send_keys(email)