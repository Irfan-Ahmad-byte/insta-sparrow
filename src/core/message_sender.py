"""
Module for managing Instagram message sending operations.
Provides a high-level interface for sending direct and group messages with proper authentication.
"""

from typing import List, Optional
import logging
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv
import src.core.instadm as instadm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MessageConfig:
    """Configuration for message sending operations."""
    retry_attempts: int = 3
    delay_between_retries: int = 60  # seconds
    batch_size: int = 50
    max_daily_messages: int = 500

@dataclass
class InstagramAccount:
    """Store Instagram account credentials."""
    username: str
    password: str
    
    @classmethod
    def from_env(cls, prefix: str) -> 'InstagramAccount':
        """
        Create InstagramAccount from environment variables.
        
        Args:
            prefix: Prefix for environment variables (e.g., 'INSTAGRAM1')
            
        Returns:
            InstagramAccount instance
        
        Raises:
            ValueError: If required environment variables are not found
        """
        username = os.getenv(f'{prefix}_USERNAME')
        password = os.getenv(f'{prefix}_PASSWORD')
        
        if not username or not password:
            raise ValueError(f"Missing credentials for {prefix}")
            
        return cls(username=username, password=password)

class InstagramMessageSender:
    """Handles Instagram message sending operations with proper authentication and error handling."""
    
    def __init__(
        self,
        account: InstagramAccount,
        headless: bool = True,
        config: Optional[MessageConfig] = None
    ):
        """
        Initialize Instagram message sender.
        
        Args:
            account: Instagram account credentials
            headless: Whether to run browser in headless mode
            config: Message sending configuration
        """
        self.account = account
        self.headless = headless
        self.config = config or MessageConfig()
        self.insta = None
        self._message_count = 0
        
    def _initialize_connection(self) -> None:
        """
        Initialize Instagram connection with retry mechanism.
        
        Raises:
            ConnectionError: If connection fails after all retries
        """
        for attempt in range(self.config.retry_attempts):
            try:
                self.insta = instadm.InstaDM(
                    username=self.account.username,
                    password=self.account.password,
                    headless=self.headless
                )
                logger.info("Successfully connected to Instagram")
                return
                
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.config.retry_attempts - 1:
                    raise ConnectionError("Failed to connect to Instagram after all retries")

    def _ensure_connection(self) -> None:
        """Ensure Instagram connection is established."""
        if not self.insta:
            self._initialize_connection()

    def _check_message_limits(self) -> None:
        """
        Check if message limits have been exceeded.
        
        Raises:
            RuntimeError: If daily message limit is exceeded
        """
        if self._message_count >= self.config.max_daily_messages:
            raise RuntimeError("Daily message limit exceeded")

    def send_direct_message(
        self,
        user: str,
        message: str,
        retry_on_failure: bool = True
    ) -> bool:
        """
        Send direct message to a single user.
        
        Args:
            user: Target username
            message: Message content
            retry_on_failure: Whether to retry on failure
            
        Returns:
            bool: Whether message was sent successfully
            
        Raises:
            ValueError: If user or message is empty
        """
        if not user or not message:
            raise ValueError("User and message must not be empty")
            
        self._check_message_limits()
        
        try:
            self._ensure_connection()
            success = self.insta.send_message(user=user, message=message)
            
            if success:
                self._message_count += 1
                logger.info(f"Successfully sent message to {user}")
                return True
                
            if retry_on_failure:
                logger.warning(f"Retrying message to {user}")
                return self.send_direct_message(user, message, False)
                
            logger.error(f"Failed to send message to {user}")
            return False
            
        except Exception as e:
            logger.error(f"Error sending message to {user}: {str(e)}")
            return False

    def send_group_message(
        self,
        users: List[str],
        message: str,
        batch_size: Optional[int] = None
    ) -> dict:
        """
        Send message to a group of users with batching.
        
        Args:
            users: List of target usernames
            message: Message content
            batch_size: Optional custom batch size
            
        Returns:
            dict: Results summary with success and failure counts
            
        Raises:
            ValueError: If users list is empty or message is empty
        """
        if not users or not message:
            raise ValueError("Users list and message must not be empty")
            
        batch_size = batch_size or self.config.batch_size
        results = {"success": 0, "failure": 0}
        
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            
            try:
                self._ensure_connection()
                self._check_message_limits()
                
                if self.insta.send_group_message(users=batch, message=message):
                    results["success"] += len(batch)
                    self._message_count += len(batch)
                    logger.info(f"Successfully sent message to batch of {len(batch)} users")
                else:
                    results["failure"] += len(batch)
                    logger.warning(f"Failed to send message to batch of {len(batch)} users")
                    
            except Exception as e:
                results["failure"] += len(batch)
                logger.error(f"Error sending batch message: {str(e)}")
                
        return results

    def get_message_stats(self) -> dict:
        """
        Get message sending statistics.
        
        Returns:
            dict: Message sending statistics
        """
        return {
            "total_messages_sent": self._message_count,
            "remaining_daily_limit": self.config.max_daily_messages - self._message_count
        }

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        if self.insta:
            try:
                self.insta.driver.quit()
            except Exception as e:
                logger.error(f"Error during cleanup: {str(e)}")

def create_sender(account_prefix: str = "INSTAGRAM1", headless: bool = True) -> InstagramMessageSender:
    """
    Factory function to create InstagramMessageSender instance.
    
    Args:
        account_prefix: Prefix for environment variables
        headless: Whether to run browser in headless mode
        
    Returns:
        InstagramMessageSender instance
    """
    load_dotenv()
    account = InstagramAccount.from_env(account_prefix)
    return InstagramMessageSender(account=account, headless=headless)

# Usage example
if __name__ == "__main__":
    try:
        with create_sender() as sender:
            # Send individual message
            sender.send_direct_message(
                user="example_user",
                message="Hello! This is a test message."
            )
            
            # Send group message
            results = sender.send_group_message(
                users=["user1", "user2", "user3"],
                message="Hello everyone! This is a group message."
            )
            
            # Print statistics
            stats = sender.get_message_stats()
            logger.info(f"Message sending statistics: {stats}")
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
