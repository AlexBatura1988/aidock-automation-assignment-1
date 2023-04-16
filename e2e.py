from src.AidockE2ETesting import AidockE2ETesting

if __name__ == '__main__':
    # Instantiate GmailAutomation class with your email
    gmail = AidockE2ETesting(email="alexautomationt@gmail.com", password="alexalex1234")

    try:
        # Perform the login process
        gmail.login()

        print(gmail.get_email_info_by_index(1))
        print(gmail.get_email_info_by_email_address('shop@amoreshop.com.ua'))
        # If login is successful, continue with the rest of your automation steps
        # ...

    except Exception as e:
        print(f"Failed to connect to Gmail: {e}")

    finally:
        # Close the browser window
        gmail.close()
