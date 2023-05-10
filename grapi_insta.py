import time
from instagrapi import Client
from itertools import islice
from typing import Dict

from copy import deepcopy
from json.decoder import JSONDecodeError
from typing import Dict, List, Tuple

from instagrapi.exceptions import (
    ClientError,
    ClientJSONDecodeError,
    ClientLoginRequired,
    ClientNotFoundError,
    UserNotFound,
)
from instagrapi.extractors import extract_user_gql, extract_user_short, extract_user_v1
from instagrapi.types import Relationship, User, UserShort
from instagrapi.utils import json_value

import csv

#user_followers(self.cl.user_id, amount=amount)

file_name = 'followers_insta.csv'

u1 = 'knightkingdelivery_dc'
pass1= 'AuCl3AR9(('

u2 = 'computertechservice1'
pass2 = '@Computer1122'

u3 = 'levajim928'
pass3 = 'levajim@928'

username = 'Knightkingdeliverysw'
password = 'AuCl3AR9('

session = f'session-{u2}'
    
competitors = ['boxboys', 'jawigrown2', 'dcweedevents_', 'dcweedeventsss', 'welit_dc_', 'welit18', 'welittogetherdc', 'highvoltage_71', 'weedwookie', 'knightkingdelivery_dc']

IG_USERNAME = u2
IG_PASSWORD = pass2

IG_CREDENTIAL_PATH = "./{IG_USERNAME}_ig_settings.json"
SLEEP_TIME = "600"  # in seconds


class Bot:
    cl = None

    def __init__(self):
        self.cl = Client()
        try:
            if os.path.exists(IG_CREDENTIAL_PATH):
                self.cl.load_settings(IG_CREDENTIAL_PATH)
                self.cl.login(IG_USERNAME, IG_PASSWORD)
            else:
                self.cl.login(IG_USERNAME, IG_PASSWORD)
                self.cl.dump_settings(IG_CREDENTIAL_PATH)
            print(f'User logged in {username}.')
        except:
            print('something went wrong')

    
    def get_followers(self, user_id=None, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followers

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        if not user_id:
            followers = self.cl.user_followers(self.cl.user_id, amount=amount)
        else:
            followers = self.cl.user_followers(user_id, amount=amount)
            
        return followers

    def get_followers_usernames(self, user_id=None, amount: int = 0) -> List[str]:
        """
        Get bot's followers usernames

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        List[str]
            List of usernames
        """
        if not user_id:
            followers = self.cl.user_followers(self.cl.user_id, amount=amount)
        else:
            followers = self.cl.user_followers(user_id, amount=amount)
        return [user.username for user in followers.values()]

    def get_following(self, user_id=None, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followed users

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        if not user_id:
            following = self.cl.user_following(self.cl.user_id, amount=amount)
        else:
            following = self.cl.user_following(user_id, amount=amount)
            
        return following

    def get_following_usernames(self, user_id=None, amount: int = 0) -> List[str]:
        """
        Get bot's followed usernames

        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf

        Returns
        -------
        List[str]
            List of usernames
        """
        if not user_id:
            following = self.cl.user_following(self.cl.user_id, amount=amount)
        else:
            following = self.cl.user_following(user_id, amount=amount)
            
        return [user.username for user in following.values()]

    def update(self):
        """
        Do something
        """
        pass


if __name__ == "__main__":
    bot = Bot()
    
    username = competitors[0].lower()
    user_id = bot.cl.user_id_from_username(username)
    
    print(f'User id for username {username}: {user_id}')

    followers = bot.get_followers_usernames(user_id, 5000)

    with open(file_name, 'a') as fl:
        writer = csv.writer(fl)
        writer.writerows([[follower.username] for follower in followers])
        

    
    
