import time
import random
import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        
        # Load the session_id from a file
        try:
            with open("session_id.txt", "r") as f:
                session_id = f.read()

            # Pass the session_id to the ChromeOptions constructor
            chrome_options.add_argument('--session-id=%s' % session_id)
        except:
            ...

        self.driver = webdriver.Remote(command_executor='http://localhost:4444', options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/direct/new/?hl=en")
        time.sleep(random.randint(10, 60))
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
        except:
            self.close()
            return 'error'
        
        if username_field and password_field:
            for k in self.username:
                username_field.send_keys(k)
            time.sleep(random.randint(2, 5))
            for p in self.password:
                password_field.send_keys(p)
        else:
            self.close()
            return 'error'
            
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
            
        return 'success'

    def send(self, usernames, message):
        time.sleep(random.randint(5, 10))
        user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        next_btn = user_pop.find_elements(By.XPATH, "//div[@role='button']")
        for btn in next_btn:
            if btn.text == 'Chat' or btn.text == 'Next':
                btn.click()
                break
                
        time.sleep(20)
        message_area = self.driver.find_element(By.XPATH, "//div[@role='textbox' and @aria-label='Message' and @aria-describedby='Message']")
        message_area.send_keys(message)
        message_area.send_keys(Keys.ENTER)
        print('Message has been sent successfully to:', usernames)
        save_file([(usernames)], 'msg_sent_users.csv')
        return True
    
    def send_message(self, usernames, message, group=False):
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
            send_msg_btn = self.driver.find_elements(By.XPATH, "//div[@role='button']")
            for btn in send_msg_btn:
                if btn.text == 'Send message':
                    btn.click()
                    break
        except:
            print("send_msg_btn not present.")
            
        time.sleep(10)

        user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        queryBox = user_pop.find_element(By.NAME, "queryBox")
        
        task_done = False

        if isinstance(usernames, list):
            for i, username in enumerate(usernames):
                time.sleep(random.randint(5, 10))
                if group:
                    for k in username:
                        queryBox.send_keys(k)
                    time.sleep(1)
                    user_select = user_pop.find_element(By.XPATH, "//div[@aria-label='Toggle selection']").click()
                else:
                    time.sleep(random.randint(10, 40))
                    if i>0:
                        new_message_btns = self.driver.find_element(By.XPATH, "//div[@aria-label='Thread list']//div[@role='button']")
                        new_message_btns.click()
                        
                    queryBox = self.driver.find_element(By.NAME, "queryBox")
                    for k in username:
                        queryBox.send_keys(k)
                    time.sleep(1)
                    user_select = user_pop.find_element(By.XPATH, "//div[@aria-label='Toggle selection']").click()
                    task_done = self.send(username, message)

        else:
            queryBox.send_keys(usernames)
            time.sleep(random.randint(5, 10))
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            try:
                user_select = user_pop.find_element(By.XPATH, "//div[@aria-label='Toggle selection']").click()
            except:
                print(f'/=/=/=/==/=/=/==/==/=/= [User {usernames} does not exist.] /=/=/=/==/=/=/==/==/=/=')
                return
                
        if task_done:
            return
                        
        self.send(usernames, message)
        time.sleep(random.uniform(2, 3))

    def close(self):
        self.driver.quit()

def save_file(data, filename):
    with open(filename, 'a') as fl:
        writer = csv.writer(fl)
        writer.writerows(data)

if __name__ == "__main__":
    usernames = []
    with open('followers_insta.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            usernames.append(row['username'])

    u4 = 'knightkingdeliverysw'
    pass4 = 'AuCl3AR9(('

    message = "Knight King Delivery delivers to age verified 21+ adults within a 75 mile radius from our headquarters on 1101 Connecticut Ave NW, Washington DC, 20036. Medical Card not required. Delivery fees are displayed on our website Knightkingdelivery.com, residents outside of Washington DC will pay more than $10 for delivery! Pickup is not an option, we offer same day and preorder delivery only with competitive pricing including these fees. Shop 90+ options for same day delivery @ https://bit.ly/shopkkd23 from 9:00AM to 12:00AM 7 days a week!"

    username = u4
    password = pass4

    target_date = datetime(2023, 5, 30, 11, 0, 0)  # Target date and time

    try_count = 1

    msg_sent_to = []
    with open('msg_sent_users.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            msg_sent_to.append(row['username'])

    def start_insta_session(try_count=1):
        if try_count > 50:
            print(f"============= [Reached maximum login attempts. Exiting.] =============")
            return 'error'

        bot = InstagramBot(username, password)
        login_re = bot.login()
        if login_re == 'error':
            time.sleep(random.uniform(3, 4) * 3600)
            return start_insta_session(try_count + 1)
        return bot


    while True:
        bot = start_insta_session()
        
        if len(usernames)<=0:
            print('+++++++++++++++ [Script ended successfully] +++++++++++++++')
            break
            
        if isinstance(bot, str) and bot == 'error':
            print('******************* [ Something has gone wrong during login. So, exiting now.] *******************')
            save_file([(usr_nm) for usr_nm in msg_sent_to], 'msg_sent_users.csv')
            break
        else:
            ...
             
        subset_size = random.randint(2, 6)
        subset = [random.choice(usernames) for _ in range(subset_size)]

        # Remove the selected usernames from the list
        usernames = [user for user in usernames if user not in subset]

        # Send messages to the selected usernames
        for user in subset:
            if user in msg_sent_to:
                subset.remove(user)
            else:
                msg_sent_to.append(user)
                ...

        bot.send_message(subset, message)

        save_file([(usr_nm) for usr_nm in msg_sent_to], 'msg_sent_users.csv')


        interval_between_sets = random.randint(2, 3) * 3600  # Random interval of 2-3 hours between sets
        # Wait for the random interval before starting the next set
        time.sleep(interval_between_sets)

        # Save the session_id
        session_id = bot.driver.session_id
        with open("session_id.txt", "w") as f:
            f.write(session_id)

        bot.close()


