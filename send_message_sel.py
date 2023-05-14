import time
import random
import selenium
from webdrivermanager.chrome import ChromeDriverManager

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        driver_manager = ChromeDriverManager()
        driver_manager.install()

        # Create a new instance of the selenium.webdriver.Chrome() class
        # Create a new instance of the ChromeOptions() class
        chrome_options = selenium.webdriver.ChromeOptions()

        # Set the headless flag
        chrome_options.add_argument('--headless')

        self.driver = selenium.webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/direct/new/?hl=en")
        time.sleep(random.randint(10, 60))
        username_field = self.driver.find_element_by_name("username")
        password_field = self.driver.find_element_by_name("password")
        username_field.send_keys(self.username)
        time.sleep(random.randint(10, 60))
        password_field.send_keys(self.password)
        time.sleep(random.randint(10, 60))
        self.driver.find_element_by_text("Log in").click()

        try:
            verification_code_field = self.driver.find_element_by_name("verificationCode")
            verification_code = input("Enter the verification code: ")
            verification_code_field.send_keys(verification_code)
            time.sleep(random.randint(10, 60))
            self.driver.find_element_by_text("Confirm").click()
        except:
            print("Verification code not required.")
        time.sleep(random.randint(10, 60))
        try:
            notification_popup = self.driver.find_element_by_xpath("//div[@role='dialog']")
            self.driver.find_element_by_text("Not Now").click()
        except:
            print("Notification popup not present.")
            
        # Get the session_id
        session_id = self.driver.session_id

        # Save the session_id to a file
        with open("session_id.txt", "w") as f:
            f.write(session_id)
            
        # Load the session_id from a file
        #with open("session_id.txt", "r") as f:
         #   session_id = f.read()

        # Pass the session_id to the ChromeOptions constructor
        #chrome_options.add_argument('--session-id=%s' % session_id)

    def send_message(self, usernames, message):
        if isinstance(usernames, list):
            for username in usernames:
                time.sleep(random.randint(5, 10))
                self.driver.find_element_by_name("queryBox").send_keys(username)
                time.sleep(random.randint(5, 10))
                self.driver.find_element_by_xpath("//div[text()='%s']" % username).click()
        else:
            self.driver.find_element_by_name("queryBox").send_keys(usernames)
            time.sleep(random.randint(5, 10))
            self.driver.find_element_by_xpath("//div[text()='%s']" % usernames).click()
        time.sleep(random.randint(5, 10))
        self.driver.find_element_by_text("Next").click()
        time.sleep(random.randint(10, 60))
        message_area = self.driver.find_element_by_xpath("//textarea[@placeholder='Message...']")
        message_area.send_keys(message)
        time.sleep(random.uniform(1,2))
        self.driver.find_element_by_text("Send").click()

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    u5 = 'devirfan.insta'

    u1 = 'knightkingdelivery_dc'
    pass1= 'AuCl3AR9(('

    u2 = 'computertechservice1'

    u4 = 'knightkingdeliverysw'
    pass4 = 'AuCl3AR9(@'

    username = u4
    password = pass4

    # Set the list of usernames to send messages to
    usernames = [u1, u2, u5]

    # Set the message to send
    message = "This is a test message."

    bot = InstagramBot(username, password)
    bot.login()
    bot.send_message(usernames, "This is a test message sent through your bot.")
    bot.close()

