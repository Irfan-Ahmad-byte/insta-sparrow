import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        time.sleep(30)
        try:
            notification_popup = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            notification_btns = notification_popup.find_elements(By.TAG_NAME, "button")
            for btn in notification_btns:
                if btn.text == 'Not Now':
                    btn.click()
                    break
        except:
            print("Notification popup not present.")
        
        time.sleep(10)
        
        try:
            # First, select the element with the role 'navigation'
            #nav_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="navigation"]')))
            
            # Now, select the next sibling element which should be the parent of 'Send message' button
            #parent = wait.until(EC.presence_of_element_located((By.XPATH, './following-sibling::div')))
            
            # Now, select the 'Send message' button within the parent element
            #button = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@role="button" and text()="Send message"]')))
            #button.click()
            
            #send_msg_btn = self.driver.find_element(By.XPATH, '//*[@id="mount_0_0_Lt"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div[2]/div/div/div/div[4]/div').click()
            #send_msg_btn_parent = self.driver.find_elements(By.XPATH, "//div[div/span[text()='Your messages']  and div/div/span[text()='Send private photos and messages to a friend or group']]")
            send_msg_btn = self.driver.find_elements(By.XPATH, "//div[@role='button']")
            for btn in send_msg_btn:
                if btn.text == 'Send message':
                    btn.click()
                    break
        except:
            print("send_msg_btn not present.")
            
        time.sleep(10)
        if isinstance(usernames, list):
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            queryBox = user_pop.find_element(By.NAME, "queryBox")
            for username in usernames:
                time.sleep(random.randint(5, 10))
                for k in username:
                    queryBox.send_keys(k)
                time.sleep(1)
                user_select = user_pop.find_elements(By.XPATH, "//div[@role='button']")
                for btn in user_select:
                    if btn.text == username:
                        btn.click()
                        break
        else:
            queryBox = self.driver.find_element(By.NAME, "queryBox")
            queryBox.send_keys(usernames)
            time.sleep(random.randint(5, 10))
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            user_select = user_pop.find_elements(By.XPATH, "//div[@role='button']")
            for btn in user_select:
                if btn.text == username:
                    btn.click()
                    break
                        
        time.sleep(random.randint(5, 10))
        user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        next_btn = user_pop.find_elements(By.XPATH, "//div[@role='button']")
        for btn in user_select:
            if btn.text == 'Chat' or btn.text == 'Next':
                btn.click()
                break
                
        time.sleep(20)
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
    bot.send_message(usernames, "This is a another test message sent through bot.")
    bot.close()

