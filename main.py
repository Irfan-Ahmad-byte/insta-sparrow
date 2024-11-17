import os
from src.core.message_sender import InstagramMessageSender
from src.utils.csv_handler import read_target_users

def get_env_variable(var_name: str) -> str:
    """Retrieve environment variable or raise an exception."""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set")
    return value

def main(group: bool = False):
    # Get credentials from environment variables
    username = get_env_variable("INSTAGRAM_USERNAME")
    password = get_env_variable("INSTAGRAM_PASSWORD")
    
    # Initialize sender with credentials
    sender = InstagramMessageSender(
        username=username,
        password=password
    )

    if group:
        # Get group users from environment variables
        group_users = [
            get_env_variable("INSTAGRAM_USER1"),
            get_env_variable("INSTAGRAM_USER2"),
            get_env_variable("INSTAGRAM_USER5")
        ]
        
        # Send group message
        sender.send_group_message(
            users=group_users,
            message='Hey! this is a test message sent to a group of users by your developer.'
        )
    else:
        # Get target user from environment variable
        target_user = get_env_variable("INSTAGRAM_TARGET_USER")
        
        # Send individual message
        sender.send_direct_message(
            user=target_user,
            message='Hey! this is a test message sent by your developer.'
        )

if __name__ == '__main__':
    main(group=True)
