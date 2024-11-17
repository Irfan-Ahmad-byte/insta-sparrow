import os
from dotenv import load_dotenv

load_dotenv()

class InstagramCredentials:
    USER1 = os.getenv('INSTAGRAM_USER1')
    PASS1 = os.getenv('INSTAGRAM_PASS1')
    USER2 = os.getenv('INSTAGRAM_USER2')
    PASS2 = os.getenv('INSTAGRAM_PASS2')
    USER3 = os.getenv('INSTAGRAM_USER3')
    PASS3 = os.getenv('INSTAGRAM_PASS3')
    USER4 = os.getenv('INSTAGRAM_USER4')
    PASS4 = os.getenv('INSTAGRAM_PASS4')
    USER5 = os.getenv('INSTAGRAM_USER5')
    PASS5 = os.getenv('INSTAGRAM_PASS5')
