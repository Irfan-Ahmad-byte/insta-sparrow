import time
import random
import csv
import signal
import instaloader

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_private(username):
    loader = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(loader.context, username)
    return profile.is_private or not profile.followed_by_viewer


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
                    
        # Load the session_id from a file
        #with open("session_id.txt", "r") as f:
         #   session_id = f.read()

        # Pass the session_id to the ChromeOptions constructor
        #chrome_options.add_argument('--session-id=%s' % session_id)

        self.driver = webdriver.Remote(command_executor='http://localhost:4444', options=chrome_options)
        #self.driver = uc.Chrome(options)
        self.driver.maximize_window()

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


    def send_message(self, usernames, message):
        self.driver.get("https://www.instagram.com/direct/new/?hl=en")
        time.sleep(random.uniform(7, 15))
        try:
            notification_popup = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            notification_btns = notification_popup.find_elements(By.TAG_NAME, "button")
            for btn in notification_btns:
                if btn.text == 'Not Now':
                    btn.click()
                    break
        except:
            print("Notification popup not present.")
        
        
        try:
            send_msg_btn = self.driver.find_elements(By.XPATH, "//div[@role='button']")
            for btn in send_msg_btn:
                if btn.text == 'Send message':
                    time.sleep(random.uniform(1, 5))
                    btn.click()
                    break
        except:
            print("send_msg_btn not present.")
            
        if isinstance(usernames, list):
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            try:
                queryBox = user_pop.find_element(By.NAME, "queryBox")
            except:
                print(f'/=/=/=/==/=/=/==/==/=/= [Query box not found.] /=/=/=/==/=/=/==/==/=/=')
                return 'error'
                
            for username in usernames:
                time.sleep(random.randint(5, 10))
                for k in username:
                    queryBox.send_keys(k)
                time.sleep(1)
                user_select = user_pop.find_elements(By.XPATH, "//div[@role='button']")
                for btn in user_select:
                    if username in btn.text:
                        try:
                            btn.click()
                            break
                        except Exception as e:
                            print(e)
                            print(f'/=/=/=/==/=/=/==/==/=/= [User Click box not found.] /=/=/=/==/=/=/==/==/=/=')
                            return 'error'
        else:
            try:
                queryBox = self.driver.find_element(By.NAME, "queryBox")
            except:
                print(f'/=/=/=/==/=/=/==/==/=/= [Query box not found.] /=/=/=/==/=/=/==/==/=/=')
                return 'error'
                
            queryBox.send_keys(usernames)
            user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            try:
                user_select = user_pop.find_elements(By.XPATH, "//div[@role='button']")
                for btn in user_select:
                    try:
                        time.sleep(random.uniform(8, 15))
                        btn.click()
                        break
                    except Exception as e:
                        print(e)
                        print(f'/=/=/=/==/=/=/==/==/=/= [User Click box not found.] /=/=/=/==/=/=/==/==/=/=')
                        return 'error'
                
            except:
                print(f'/=/=/=/==/=/=/==/==/=/= [User {usernames} does not exist.] /=/=/=/==/=/=/==/==/=/=')
                return 'error'
                        
        user_pop = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        next_btn = user_pop.find_elements(By.XPATH, "//div[@role='button']")
        for btn in next_btn:
            if btn.text == 'Chat' or btn.text == 'Next':
                time.sleep(random.randint(5, 10))
                btn.click()
                break
                
        time.sleep(random.uniform(8, 15))
        message_area = self.driver.find_element(By.XPATH, "//div[@role='textbox' and @aria-label='Message' and @aria-describedby='Message']")
        message_area.send_keys(message)
        message_area.send_keys(Keys.ENTER)
        print('Message has been sent successfully to : ', usernames)
        try:
            save_file([(usr_nm)  for usr_nm in usernames], 'msg_sent_users.csv')
        except:
            save_file([(usernames)], 'msg_sent_users.csv')
        #self.driver.find_element(By.XPATH, "//div[text()='Send']").click()
        return 'success'

    def close(self):
        self.driver.quit()

def save_file(data, filename):
    with open(filename, 'a') as fl:
        writer = csv.writer(fl)
        writer.writerows(data)

if __name__ == "__main__":
    bot = None
    
    def signal_handler(sig, frame):
        if bot is not None:
            bot.close()
        print("Script terminated")
        exit(0)
        
    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    u4 = 'knightkingdeliverysw'
    pass4 = 'AuCl3AR9(#'
    
    # Set the message to send
    message = "Knight King Delivery delivers to age verified 21+ adults within a 75 mile radius from our headquarters on 1101 Connecticut Ave NW, Washington DC, 20036. Medical Card not required. Delivery fees are displayed on our website Knightkingdelivery.com, residents outside of Washington DC will pay more than $10 for delivery! Pickup is not an option, we offer same day and preorder delivery only with competitive pricing including these fees. Shop 90+ options for same day delivery @ https://bit.ly/shopkkd23 from 9:00AM to 12:00AM 7 days a week!"

    username = u4
    password = pass4
    
    target_date = datetime(2023, 5, 30, 11, 0, 0)  # Target date and time
    
    try_count = 1
    
    def start_insta_session():
        try:
            bot.close()
        except:
            ...
        global try_count
        bot = InstagramBot(username, password)
        login_re = bot.login()
        if login_re=='error':
            time.sleep(random.uniform(3,4)*3600)
            try_count += 1
            if try_count>50:
                return login_re
            print(f'============= [trying to login again. Login attempt: {try_count}] =============')
            start_insta_session()
        return bot
        
    while True:
        # Load the usernames from the file
        usernames = []
        with open('followers_insta.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                usernames.append(row['username'])
        
        msg_sent_to = []
        with open('msg_sent_users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                msg_sent_to.append(row['username'])
            
        usernames = [user for user in usernames if user not in msg_sent_to]
        if len(usernames)<=0:
            break
            
        bot = start_insta_session()
        
        if isinstance(bot, str) and bot=='error':
            print('******************* [ Something has gone wrong during login. So, exiting now.] *******************')
            save_file([(usr_nm)  for usr_nm in msg_sent_to], 'msg_sent_users.csv')
            break

        # Select a random subset of usernames to send messages to
        subset_size = random.randint(5, 8)
        subset = [random.choice(usernames) for _ in range(subset_size)]

        # Send messages to the selected usernames
        for user in subset:
            if user not in msg_sent_to:
                sent = bot.send_message(user, message)
                if sent == 'error':
                    bot.close()
                    time.sleep(random.uniform(60, 80)*30)
                    bot = start_insta_session()
                else:
                    msg_sent_to.append(user)
            else:
                ...
                
        try:
            bot.close()
        except:
            ...
            
        interval_between_sets = random.uniform(1,2) * 3600  # Random interval of 2-3 hours between sets
        # Wait for the random interval before starting the next set
        time.sleep(interval_between_sets)
        

