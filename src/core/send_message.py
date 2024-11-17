"""
Module for managing Instagram message sending operations with multiple accounts.
Provides functionality for sending direct and group messages using a pool of Instagram accounts.
"""

import csv
from typing import List, Optional, Dict
from pathlib import Path
import os
from dataclasses import dataclass
import logging
from dotenv import load_dotenv
import src.core.instadm as instadm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_operations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class InstagramAccount:
    """Store Instagram account credentials and session information."""
    username: str
    password: str
    session_name: Optional[str] = None

    def __post_init__(self):
        """Set session name if not provided."""
        if not self.session_name:
            self.session_name = f'session-{self.username}'

    @classmethod
    def from_env(cls, prefix: str) -> 'InstagramAccount':
        """
        Create InstagramAccount from environment variables.
        
        Args:
            prefix: Environment variable prefix (e.g., 'INSTAGRAM1')
            
        Returns:
            InstagramAccount instance
        """
        load_dotenv()
        username = os.getenv(f'{prefix}_USERNAME')
        password = os.getenv(f'{prefix}_PASSWORD')
        
        if not username or not password:
            raise ValueError(f"Missing credentials for {prefix}")
            
        return cls(username=username, password=password)

class InstagramAccountPool:
    """Manages a pool of Instagram accounts for message sending."""
    
    def __init__(self, num_accounts: int = 5):
        """
        Initialize account pool.
        
        Args:
            num_accounts: Number of accounts to manage
        """
        self.accounts: List[InstagramAccount] = []
        self._load_accounts(num_accounts)

    def _load_accounts(self, num_accounts: int) -> None:
        """Load Instagram accounts from environment variables."""
        for i in range(1, num_accounts + 1):
            try:
                account = InstagramAccount.from_env(f'INSTAGRAM{i}')
                self.accounts.append(account)
                logger.info(f"Loaded account: {account.username}")
            except ValueError as e:
                logger.warning(f"Failed to load account {i}: {str(e)}")

    def get_account(self, index: int) -> InstagramAccount:
        """
        Get account by index.
        
        Args:
            index: Account index
            
        Returns:
            InstagramAccount instance
        
        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < len(self.accounts):
            raise IndexError("Account index out of range")
        return self.accounts[index]

class TargetUserManager:
    """Manages target user data from CSV files."""
    
    def __init__(self, data_dir: Path = Path('../../data')):
        """
        Initialize target user manager.
        
        Args:
            data_dir: Directory containing user data files
        """
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_users(self, filename: str = 'followers_insta.csv') -> List[str]:
        """
        Load target users from CSV file.
        
        Args:
            filename: Name of CSV file
            
        Returns:
            List of usernames
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        file_path = self.data_dir / filename
        target_users = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as fl:
                reader = csv.reader(fl)
                for row in reader:
                    if row and row[0].strip():
                        target_users.append(row[0].strip())
                        
            logger.info(f"Loaded {len(target_users)} target users from {filename}")
            return target_users
            
        except FileNotFoundError:
            logger.error(f"Target user file not found: {file_path}")
            raise

class MessageSender:
    """Handles Instagram message sending operations."""
    
    def __init__(
        self,
        account: InstagramAccount,
        headless: bool = True,
        retry_attempts: int = 3
    ):
        """
        Initialize message sender.
        
        Args:
            account: Instagram account credentials
            headless: Whether to run browser in headless mode
            retry_attempts: Number of retry attempts for failed operations
        """
        self.account = account
        self.headless = headless
        self.retry_attempts = retry_attempts
        self.insta = None

    def _initialize_connection(self) -> None:
        """Initialize Instagram connection with retry mechanism."""
        for attempt in range(self.retry_attempts):
            try:
                self.insta = instadm.InstaDM(
                    username=self.account.username,
                    password=self.account.password,
                    headless=self.headless
                )
                logger.info(f"Successfully connected to Instagram as {self.account.username}")
                return
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.retry_attempts - 1:
                    raise ConnectionError("Failed to connect after all attempts")

    def send_direct_message(self, user: str, message: str) -> bool:
        """
        Send direct message to a single user.
        
        Args:
            user: Target username
            message: Message content
            
        Returns:
            bool: Whether message was sent successfully
        """
        try:
            if not self.insta:
                self._initialize_connection()
                
            success = self.insta.sendMessage(user=user, message=message)
            if success:
                logger.info(f"Successfully sent message to {user}")
            else:
                logger.warning(f"Failed to send message to {user}")
            return success
            
        except Exception as e:
            logger.error(f"Error sending message to {user}: {str(e)}")
            return False

    def send_group_message(self, users: List[str], message: str) -> bool:
        """
        Send message to a group of users.
        
        Args:
            users: List of target usernames
            message: Message content
            
        Returns:
            bool: Whether message was sent successfully
        """
        try:
            if not self.insta:
                self._initialize_connection()
                
            success = self.insta.sendGroupMessage(users=users, message=message)
            if success:
                logger.info(f"Successfully sent group message to {len(users)} users")
            else:
                logger.warning("Failed to send group message")
            return success
            
        except Exception as e:
            logger.error(f"Error sending group message: {str(e)}")
            return False

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

class MessageOperations:
    """High-level message operations manager."""
    
    def __init__(self):
        """Initialize message operations."""
        self.account_pool = InstagramAccountPool()
        self.user_manager = TargetUserManager()

    def send_message(self, group: bool = False) -> Dict[str, int]:
        """
        Send messages using configured accounts.
        
        Args:
            group: Whether to send group messages
            
        Returns:
            Dict containing operation statistics
        """
        stats = {"success": 0, "failure": 0}
        
        try:
            # Use account 4 as default (can be configured)
            account = self.account_pool.get_account(3)  # Index 3 for account 4
            
            with MessageSender(account=account) as sender:
                if group:
                    # Send group message
                    users = [
                        self.account_pool.get_account(1).username,  # Account 2
                        self.account_pool.get_account(0).username,  # Account 1
                        self.account_pool.get_account(4).username   # Account 5
                    ]
                    
                    success = sender.send_group_message(
                        users=users,
                        message="Hey! this is a test message sent to a group of users by your developer."
                    )
                    stats["success" if success else "failure"] += 1
                    
                else:
                    # Send individual message
                    success = sender.send_direct_message(
                        user=self.account_pool.get_account(0).username,  # Account 1
                        message="Hey! this is a test message sent by your developer."
                    )
                    stats["success" if success else "failure"] += 1
                    
            return stats
            
        except Exception as e:
            logger.error(f"Error in message operations: {str(e)}")
            stats["failure"] += 1
            return stats

def main():
    """Main execution function."""
    try:
        operations = MessageOperations()
        stats = operations.send_message(group=True)
        logger.info(f"Message sending statistics: {stats}")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == '__main__':
    main()
