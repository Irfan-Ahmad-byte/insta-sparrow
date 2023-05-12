import selenium
from webdrivermanager.chrome import ChromeDriverManager

# Set the username and password
u5 = 'devirfan.insta'
pass5 = 'IL@tmys@lf1@insta'

u1 = 'knightkingdelivery_dc'
pass1= 'AuCl3AR9(('

u2 = 'computertechservice1'
pass2 = '@Computer1122'

u4 = 'knightkingdeliverysw'
pass4 = 'AuCl3AR9(@'

username = u5
password = pass5

# Set the list of usernames to send messages to
usernames = [u1, u2, u4]

# Set the message to send
message = "This is a test message."

driver_manager = ChromeDriverManager()
driver_manager.install()

# Create a new instance of the selenium.webdriver.Chrome() class
# Create a new instance of the ChromeOptions() class
chrome_options = selenium.webdriver.ChromeOptions()

# Set the headless flag
chrome_options.add_argument('--headless')

driver = selenium.webdriver.Chrome(options=chrome_options)

# Navigate to the Instagram Direct Messenger page
driver.get("https://www.instagram.com/direct/new/?hl=en")

# Find the input fields with names username and password
username_field = driver.find_element_by_name("username")
password_field = driver.find_element_by_name("password")

# Enter the username and password
username_field.send_keys(username)
password_field.send_keys(password)

# Click the Log in button
driver.find_element_by_text("Log in").click()

# Wait for a random time between 10 and 60 seconds
time.sleep(random.randint(10, 60))

# Check if there is a verification field
verification_code_field = driver.find_element_by_name("verificationCode")

# If there is a verification field, ask for the verification code in the terminal
if verification_code_field is not None:
    verification_code = input("Enter the verification code: ")
    verification_code_field.send_keys(verification_code)
    driver.find_element_by_text("Confirm").click()

# Wait for a random time between 10 and 60 seconds
time.sleep(random.randint(10, 60))

# Check if there is a notification popup
notification_popup = driver.find_element_by_xpath("//div[@role='dialog']")

# If there is a notification popup, click the Not Now button
try:
    driver.find_element_by_text("Not Now").click()
except:
    ...    

# Wait for a random time between 10 and 60 seconds
time.sleep(random.randint(10, 60))

# Find the input field with name 'queryBox'
query_box = driver.find_element_by_name("queryBox")

# Enter the username to which we want to send a message
for username in usernames:
    query_box.send_keys(username)
    time.sleep(random.randint(20, 90))
    driver.find_element_by_xpath("//div[text()='%s']" % username).click()

# Click the Next button
driver.find_element_by_text("Next").click()

# Wait for a random time between 10 and 60 seconds
time.sleep(random.randint(10, 60))

# Find the textarea which has placeholder 'Message...'
message_area = driver.find_element_by_xpath("//textarea[@placeholder='Message...']")

# Enter the message
message_area.send_keys(message)

# Wait for a random time between 10 and 60 seconds
time.sleep(random.randint(10, 60))

# Find the element with text 'Send', click on it to send the message
driver.find_element_by_text("Send").click()

# Close the driver
driver.quit()

