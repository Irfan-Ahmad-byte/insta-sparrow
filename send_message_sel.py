import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        # Create a new instance of the selenium.webdriver.Chrome() class
        # Create a new instance of the ChromeOptions() class
        chrome_options = webdriver.ChromeOptions()

        # Set the headless flag
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        
        #options = uc.ChromeOptions()
        #options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"])

        self.driver = webdriver.Remote(command_executor='http://localhost:4444', options=chrome_options)
        #self.driver = uc.Chrome(options)

    def login(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(random.randint(10, 60))
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        for k in self.username:
            username_field.send_keys(k)
        time.sleep(random.randint(2, 5))
        for p in self.password:
            password_field.send_keys(p)
        time.sleep(random.randint(2, 6))
        eles = self.driver.find_elements(By.TAG_NAME, "button")
        for ele in eles:
            if ele.text == 'Log in':
                ele.click()
                break

        try:
            verification_code_field = self.driver.find_element(By.NAME, "verificationCode")
            verification_code = input("Enter the verification code: ")
            verification_code_field.send_keys(verification_code)
            time.sleep(random.randint(10, 60))
            self.driver.find_element(By.XPATh, "//div[text()='Confirm']").click()
        except:
            print("Verification code not required.")
        time.sleep(random.randint(10, 60))
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
        self.driver.get("https://www.instagram.com/direct/new/?hl=en")
        time.sleep(60)
        try:
            notification_popup = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            notification_btns = notification_popup.find_elements(By.TAG_NAME, "button")
            for btn in notification_btns:
                if btn.text == 'Not Now':
                    btn.click()
                    break
        except:
            print("Notification popup not present.")
        
        time.sleep(60)
        
        try:
            send_msg_btn = self.driver.find_element(By.XPATH, "//div[@role='button']")
            for btn in send_msg_btn:
                if btn.text == 'Send message':
                    btn.click()
                    break
        except:
            print("Notification popup not present.")
            
        time.sleep(30)
        if isinstance(usernames, list):
            for username in usernames:
                time.sleep(random.randint(5, 10))
                queryBox = self.driver.find_element(By.NAME, "queryBox")
                for k in username:
                    queryBox.send_keys(k)
                time.sleep(random.randint(5, 10))
                user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                user_select = user_pop.find_element(By.XPATH, "//div[@role='button']")
                for btn in user_select:
                    if btn.text == username:
                        btn.click()
                        break
        else:
            queryBox = self.driver.find_element(By.NAME, "queryBox")
            queryBox.send_keys(usernames)
            time.sleep(random.randint(5, 10))
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            user_select = user_pop.find_element(By.XPATH, "//div[@role='button']")
            for btn in user_select:
                if btn.text == username:
                    btn.click()
                    break
                        
        time.sleep(random.randint(5, 10))
        user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        next_btn = user_pop.find_element(By.XPATH, "//div[@role='button']")
        for btn in user_select:
            if btn.text == 'Chat' or btn.text == 'Next':
                btn.click()
                break
                
        time.sleep(60)
        message_area = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
        message_area.send_keys(message)
        message_area.send_keys(Keys.ENTER)
        #time.sleep(random.uniform(1,2))
        #self.driver.find_element(By.XPATH, "//div[text()='Send']").click()

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    u5 = 'devirfan.insta'

    u1 = 'knightkingdelivery_dc'
    pass1= 'AuCl3AR9(('

    u2 = 'computertechservice1'

    u4 = 'knightkingdeliverysw'
    pass4 = 'AuCl3AR9(@'
    
    u6 = 'gracias1984'

    username = u4
    password = pass4

    # Set the list of usernames to send messages to
    usernames = [u1, u2, u5, u6]

    # Set the message to send
    message = "This is a test message."

    bot = InstagramBot(username, password)
    bot.login()
    bot.send_message(usernames, "This is a test message sent through your bot.")
    bot.close()

