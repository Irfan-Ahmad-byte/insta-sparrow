import time
import instaloader
from itertools import islice
import csv


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

# Get instance
#L = instaloader.Instaloader()

# Optionally, login or load session
#L.login(USER, PASSWORD)        # (login)
#L.interactive_login(USER)      # (ask password on terminal)
#L.load_session_from_file(USER) # (load session created w/
                               #  `instaloader -l USERNAME`)
                               
                               
def get_followers_with_retry(profile, start_index=0, max_followers=400, max_retries=3, delay_between_retries=60*20):
    followers = []
    retries = 0

    while retries < max_retries:
        try:
            followers_iterator = profile.get_followers()
            if max_followers is not None:
                max_followers += start_index
                followers_iterator = islice(followers_iterator, start_index, max_followers)

            for follower in followers_iterator:
                with open(file_name, 'a') as fl:
                    writer = csv.writer(fl)
                    writer.writerow([follower.username])
                followers.append([follower.username])
                # Add a delay between requests to avoid rate limits
                #time.sleep(1)

            return f'{len(followers)} follwoers added.'
        except instaloader.exceptions.QueryReturnedBadRequestException:
            retries += 1
            if retries < max_retries:
                print(f"Error occurred, retrying... ({retries}/{max_retries})")
                time.sleep(delay_between_retries)
            else:
                print("Max retries reached. Aborting.")
                return Exception

    return f'{len(followers)} follwoers added.'
    
competitors = ['boxboys', 'jawigrown2', 'dcweedevents_', 'dcweedeventsss', 'welit_dc_', 'welit18', 'welittogetherdc', 'highvoltage_71', 'weedwookie', 'knightkingdelivery_dc']

with instaloader.Instaloader() as L:
    L.load_session_from_file(username, session)
    try:
        profile = instaloader.Profile.from_username(L.context, competitors[0])
        response = get_followers_with_retry(profile, start_index=0, max_followers=None, max_retries=3, delay_between_retries=60*20)
        print(response)
    except Exception as e:
        print(e)
    
    
    
