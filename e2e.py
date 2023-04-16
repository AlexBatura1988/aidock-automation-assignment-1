from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GmailAutomation:

    def __init__(self, email):
        self.email = email
        self.password = "alexalex1234"
        self.driver = None

    def login(self):
        try:
            # Create Chrome Service object with ChromeDriverManager
            chrome_service = ChromeService(executable_path=ChromeDriverManager().install())

            # Create Chrome WebDriver with Chrome Service
            self.driver = webdriver.Chrome(service=chrome_service)

            # Navigate to Gmail website
            self.driver.get("https://www.gmail.com")

            # Enter email address
            email_input = self.driver.find_element(By.ID, "identifierId")
            email_input.send_keys(self.email)

            # Click Next button
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()

            # Wait for password input to be visible
            password_input = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            # Enter password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)

            # Click Next button
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()

        except Exception as e:
            print(f"Failed to login to Gmail: {e}")

    def close(self):
        # Close the browser window
        if self.driver:
            self.driver.quit()
            self.driver = None


if __name__ == '__main__':
    # Instantiate GmailAutomation class with your email
    gmail = GmailAutomation(email="alexautomationt@gmail.com")

    try:
        # Perform the login process
        gmail.login()

        # If login is successful, continue with the rest of your automation steps
        # ...

    except Exception as e:
        print(f"Failed to connect to Gmail: {e}")

    finally:
        # Close the browser window
        gmail.close()
