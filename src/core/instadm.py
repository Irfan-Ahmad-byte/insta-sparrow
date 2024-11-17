"""
Module for handling Instagram Direct Message automation using Selenium.
Provides functionality for sending individual and group messages with rate limiting.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import sqlite3
from pathlib import Path
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class InstagramSelectors:
    """Store Instagram web element selectors."""
    accept_cookies: str = "//button[text()='Allow essential and optional cookies']"
    accept_cookies_post_login: str = "//button[text()='Allow all cookies']"
    home_to_login_button: str = "//button[text()='Log In']"
    username_field: str = "username"
    password_field: str = "password"
    button_login: str = "//button/*[text()='Log In']"
    login_check: str = "//*[@aria-label='Home'] | //button[text()='Save Info'] | //button[text()='Not Now']"
    search_user: str = "queryBox"
    select_user: str = '//div[text()="{}"]'
    name: str = "((//div[@aria-labelledby]/div/span//img[@data-testid='user-avatar'])[1]//..//..//..//div[2]/div[2]/div)[1]"
    next_button: str = "//button/*[text()='Next']"
    textarea: str = "//textarea[@placeholder]"
    send: str = "//button[text()='Send']"

class InstagramDM:
    """Handles Instagram Direct Message automation using Selenium."""

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = True,
        instapy_workspace: Optional[str] = None,
        profile_dir: Optional[str] = None
    ):
        """
        Initialize Instagram DM automation.

        Args:
            username: Instagram username
            password: Instagram password
            headless: Whether to run browser in headless mode
            instapy_workspace: Path to InstaPy workspace
            profile_dir: Chrome profile directory
        """
        self.selectors = InstagramSelectors()
        self.driver = self._initialize_driver(headless, profile_dir)
        self.db_connection = self._initialize_database(instapy_workspace)
        
        try:
            self.login(username, password)
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    def _initialize_driver(
        self,
        headless: bool,
        profile_dir: Optional[str]
    ) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with specified options."""
        options = webdriver.ChromeOptions()
        
        if profile_dir:
            options.add_argument(f"user-data-dir=profiles/{profile_dir}")
        
        if headless:
            options.add_argument("--headless")

        # Mobile emulation settings
        mobile_emulation = {
            "userAgent": ('Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) '
                        'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/99.0.4844.51 '
                        'Mobile Safari/535.19')
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=options
        )
        driver.set_window_position(0, 0)
        driver.set_window_size(414, 736)
        
        return driver

    def _initialize_database(self, workspace: Optional[str]) -> Optional[sqlite3.Connection]:
        """Initialize SQLite database for message tracking."""
        if not workspace:
            return None

        db_path = Path(workspace) / "InstaPy/db/instapy.db"
        conn = sqlite3.connect(str(db_path))
        
        # Create message table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS message (
                username TEXT NOT NULL UNIQUE,
                message TEXT DEFAULT NULL,
                sent_message_at TIMESTAMP
            )
        """)
        
        return conn

    def _wait_for_element(
        self,
        selector: str,
        by: str,
        timeout: int = 10
    ) -> bool:
        """
        Wait for element to be present on page.

        Args:
            selector: Element selector
            by: Selector type (xpath, name, etc.)
            timeout: Maximum wait time in seconds

        Returns:
            bool: Whether element was found
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, selector))
            )
            return True
        except TimeoutException:
            return False

    def _get_element(self, selector: str, by: str):
        """Get element using specified selector."""
        return self.driver.find_element(by_type, selector)

    def _random_sleep(self, min_seconds: int = 3, max_seconds: int = 7) -> None:
        """Sleep for random duration to avoid detection."""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def login(self, username: str, password: str) -> None:
        """
        Log into Instagram account.

        Args:
            username: Instagram username
            password: Instagram password
        """
        self.driver.get('https://instagram.com/?hl=en')
        self._random_sleep()

        # Handle cookies popup
        if self._wait_for_element(self.selectors.accept_cookies, 'xpath'):
            self._get_element(self.selectors.accept_cookies, 'xpath').click()
            self._random_sleep()

        # Click login button if needed
        if self._wait_for_element(self.selectors.home_to_login_button, 'xpath'):
            self._get_element(self.selectors.home_to_login_button, 'xpath').click()
            self._random_sleep(5, 7)

        # Enter credentials
        if not self._wait_for_element(self.selectors.username_field, 'name'):
            raise Exception("Login failed: username field not visible")

        self.driver.find_element_by_name(self.selectors.username_field).send_keys(username)
        self.driver.find_element_by_name(self.selectors.password_field).send_keys(password)
        self._get_element(self.selectors.button_login, 'xpath').click()
        self._random_sleep()

        # Handle post-login
        if self._wait_for_element(self.selectors.login_check, 'xpath'):
            logger.info("Login successful")
            if self._wait_for_element(self.selectors.accept_cookies_post_login, 'xpath'):
                self._get_element(self.selectors.accept_cookies_post_login, 'xpath').click()
                self._random_sleep(2, 4)
        else:
            raise Exception("Login failed: Incorrect credentials")

    def create_custom_greeting(self, greeting: str) -> str:
        """Create personalized greeting using recipient's name."""
        if self._wait_for_element(self.selectors.name, "xpath"):
            user_name = self._get_element(self.selectors.name, "xpath").text
            if user_name:
                return f"{greeting} {user_name},\n\n"
        return f"{greeting},\n\n"

    def type_message(self, message: str) -> None:
        """Type and send message."""
        if self._wait_for_element(self.selectors.next_button, "xpath"):
            self._get_element(self.selectors.next_button, "xpath").click()
            self._random_sleep()

        if self._wait_for_element(self.selectors.textarea, "xpath"):
            textarea = self._get_element(self.selectors.textarea, "xpath")
            for char in message:
                textarea.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

        if self._wait_for_element(self.selectors.send, "xpath"):
            self._get_element(self.selectors.send, "xpath").click()
            self._random_sleep(3, 5)
            logger.info("Message sent successfully")

    def send_message(
        self,
        username: str,
        message: str,
        greeting: Optional[str] = None
    ) -> bool:
        """
        Send direct message to a user.

        Args:
            username: Recipient's username
            message: Message content
            greeting: Optional custom greeting

        Returns:
            bool: Whether message was sent successfully
        """
        logger.info(f"Sending message to {username}")
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self._random_sleep(5, 7)

        try:
            # Search for user
            self._wait_for_element(self.selectors.search_user, "name")
            search_field = self._get_element(self.selectors.search_user, "name")
            search_field.send_keys(username)
            self._random_sleep(7, 10)

            # Add greeting if provided
            full_message = message
            if greeting:
                full_message = self.create_custom_greeting(greeting) + message

            # Select user and send message
            elements = self.driver.find_elements_by_xpath(
                self.selectors.select_user.format(username)
            )
            self._random_sleep(50, 60)

            if elements:
                elements[0].click()
                self._random_sleep()
                self.type_message(full_message)

                # Record message in database
                if self.db_connection:
                    cursor = self.db_connection.cursor()
                    cursor.execute(
                        'INSERT INTO message (username, message) VALUES(?, ?)',
                        (username, message)
                    )
                    self.db_connection.commit()

                self._random_sleep(50, 60)
                return True
            else:
                logger.warning(f"User {username} not found")
                return False

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def send_group_message(self, users: List[str], message: str) -> bool:
        """
        Send message to multiple users.

        Args:
            users: List of usernames
            message: Message content

        Returns:
            bool: Whether message was sent successfully
        """
        logger.info(f"Sending group message to {len(users)} users")
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self._random_sleep(5, 7)

        try:
            users_found = []
            for user in users:
                self._wait_for_element(self.selectors.search_user, "name")
                search_field = self._get_element(self.selectors.search_user, "name")
                search_field.send_keys(user)
                self._random_sleep()

                elements = self.driver.find_elements_by_xpath(
                    self.selectors.select_user.format(user)
                )
                self._random_sleep(50, 60)

                if elements:
                    elements[0].click()
                    self._random_sleep()
                    users_found.append(user)
                else:
                    logger.warning(f"User {user} not found")

            if users_found:
                self.type_message(message)

                # Record messages in database
                if self.db_connection:
                    cursor = self.db_connection.cursor()
                    cursor.executemany(
                        'INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)',
                        [(user, message) for user in users_found]
                    )
                    self.db_connection.commit()

                return True
            return False

        except Exception as e:
            logger.error(f"Error sending group message: {e}")
            return False

    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'driver'):
            self.driver.quit()
        if hasattr(self, 'db_connection'):
            self.db_connection.close()
