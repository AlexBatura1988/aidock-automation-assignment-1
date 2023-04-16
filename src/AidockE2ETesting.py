from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GMAIL_URL = "https://www.gmail.com"
NON_SELECTED_TAB_COLOR = 'rgba(0, 0, 0, 0)'

class AidockE2ETesting:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
        self.primary_emails = None # class cache

    def open_gmail(self):
        # Create Chrome WebDriver with Chrome Service
        self.driver = webdriver.Chrome(service=self.chrome_service)

        # Navigate to Gmail website
        self.driver.get(GMAIL_URL)

    def login(self):
        # Task #5

        self.open_gmail()
        # Enter email address
        email_input = self.driver.find_element(By.ID, "identifierId")
        email_input.send_keys(self.email)

        # Click Next button
        next_button = self.driver.find_element(By.ID, "identifierNext")
        next_button.click()

        # Wait for password input to be visible
        password_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "Passwd"))
        )
        # Enter password
        password_input.send_keys(self.password)

        # Click Next button
        next_button = self.driver.find_element(By.ID, "passwordNext")
        next_button.click()

        # Waiting for the gmail page
        some_table = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))
        )

    def is_primary_tab_selected(self) -> bool:
        # Task #6
        # the selected tab contains a pseudo before element with a background color so we want to use js to compute the color
        primary_pseudo_elements_color =  self.driver.execute_script("return window.getComputedStyle(document.querySelector('div[role=tab]'), ':before').getPropertyValue('background-color')")
        return primary_pseudo_elements_color != NON_SELECTED_TAB_COLOR

    def open_primary_tab(self):
        # Task #7
        if not self.is_primary_tab_selected():
            primary_element = self.driver.find_element(By.CSS_SELECTOR, 'div[role=tab]') # assuming the first tab is the primary tab
            primary_element.click()

    def get_primary_emails(self):
        if not self.primary_emails:
            self.open_primary_tab()
            self.primary_emails = self.driver.find_elements(By.CSS_SELECTOR, 'tr[role=row]')

        return self.primary_emails

    def get_emails_count(self):
        # Task #8
        return len(self.get_primary_emails())
    
    def get_sender_info(self, email_ele):
        sender_container_ele, subject_ele, *_ =  email_ele.find_elements(By.CSS_SELECTOR, 'td[role=gridcell]')
        sender_ele = sender_container_ele.find_element(By.CSS_SELECTOR, 'span span')

        email_info = dict(
            sender_name=sender_ele.get_attribute('name'),
            sender_email=sender_ele.get_attribute('email'),
            subject=subject_ele.get_attribute('innerText'),
        )
        return email_info
    
    def get_email_info_by_index(self, email_number):
        # Task #9
        total_emails = self.get_emails_count()
        assert 0 <= email_number < total_emails, 'the email number is not valid'
        emails = self.get_primary_emails()
        return self.get_sender_info(emails[email_number])
    
    def get_email_info_by_email_address(self, email_address):
        # Task 10
        # convert every email element to email info and filter out non matching emails
        return list(filter(lambda email_info: email_info['sender_email'] == email_address ,map(self.get_sender_info, self.get_primary_emails())))


    def close(self):
        # Close the browser window
        if self.driver:
            self.driver.quit()
            self.driver = None
