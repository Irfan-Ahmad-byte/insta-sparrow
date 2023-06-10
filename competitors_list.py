import time
import instaloader
from itertools import islice, chain
import csv
import random


file_name = 'followers_insta.csv'

batch_size = 500
min_delay = 1.5 * 24 * 60 * 60  # 1.5 days in seconds
max_delay = 2.5 * 24 * 60 * 60  # 2.5 days in seconds

u1 = 'knightkingdelivery_dc'
pass1= 'AuCl3AR9(('

u2 = 'computertechservice1'
pass2 = '@Computer1122'


u4 = 'knightkingdeliverysw'
pass4 = 'AuCl3AR9(('

u5 = 'devirfan.insta'
pass5 = 'IL@tmys@lf1@insta'

username= u4
session = f'session-{username}'

# Get instance
#L = instaloader.Instaloader()

# Optionally, login or load session
#L.login(USER, PASSWORD)        # (login)
#L.interactive_login(USER)      # (ask password on terminal)
#L.load_session_from_file(USER) # (load session created w/
                               #  `instaloader -l USERNAME`)
                               
                               
def clean_ghost_followers(profile, followers):
    likes = set()
    for post in profile.get_posts():
        likes = likes | set(post.get_likes())
    
    cleaned_followers = followers.intersection(likes)
    
    return cleaned_followers


def get_followers(usernames:list):
    # get follower iterators of each username in the list and clean from the ghost followers
    cleaned_followers = []
    for username in usernames:
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            followers_iterator = set(profile.get_followers())
            followers_iterator = clean_ghost_followers(profile, followers_iterator)
            cleaned_followers = chain(cleaned_followers, followers_iterator)
            
        except:
            print(f'========== The user {username} does not exist. ============')
            
    return cleaned_followers


def get_followers_with_retry(followers_iterator:list, start_index=0, max_followers:int=400, max_retries:int=3, delay_between_retries=60*20):
    followers = []
    retries = 0
    
    while retries < max_retries:
        try:
            if max_followers is not None:
                max_followers += start_index
                followers_iterator = islice(followers_iterator, start_index, max_followers)
                
            for follower in followers_iterator:
                try:
                    followers.append([follower.username])
                except:
                    try:
                        instaloader.save("resume_information.json", followers_iterator.freeze())
                    except Exception as e:
                        print(e)
                        return followers
                    return followers
                # Add a delay between requests to avoid rate limits
                #time.sleep(1)

            return followers
        except instaloader.exceptions.QueryReturnedBadRequestException:
            retries += 1
            if retries < max_retries:
                print(f"Error occurred, retrying... ({retries}/{max_retries})")
                time.sleep(delay_between_retries)
            else:
                print("Max retries reached. Aborting.")
                return followers

    return followers
    
competitors = ['boxboys', 'jawigrown2', 'dcweedevents_', 'dcweedeventsss', 'welit_dc_', 'welit18', 'welittogetherdc', 'highvoltage_71', 'weedwookie', 'knightkingdelivery_dc']


followers = []
with instaloader.Instaloader() as L:
    L.load_session_from_file(username, session)
    #L.login(u1, pass1)        # (login)
    try:
        cleaned_followers_iterators = get_followers(competitors)
        
        patch_count = round(len(list(cleaned_followers_iterators))/500)
        
        for i in range(patch_count):
            if i==patch_count-1:
                break
            followers = get_followers_with_retry(cleaned_followers_iterators, start_index=500*i, max_followers=500, max_retries=3, delay_between_retries=60*20)
        
        if len(followers)>0:
            with open(file_name, 'a') as fl:
                writer = csv.writer(fl)
                writer.writerows(followers)

        print(f'{len(followers)} follwoers added.')
    
    except:
        ...






