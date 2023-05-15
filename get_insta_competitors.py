import os
import time
import instaloader
from itertools import islice
import csv
import random
import getpass

# Define file path for the CSV file
file_name = os.path.join('/app', 'data', 'followers_insta.csv')

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

# Define a function to write followers to the CSV file
def write_followers_to_csv(followers):
    with open(file_name, 'a') as fl:
        writer = csv.writer(fl)
        writer.writerows(followers)
        

# Define user credentials
user_credentials = {
    'knightkingdelivery_dc': '***YOUR_SECRET***',
    'computertechservice1': '***YOUR_SECRET***',
    'levajim928': '***YOUR_SECRET***',
    'knightkingdeliverysw': '***YOUR_SECRET***',
    'devirfan.insta': '***YOUR_SECRET***',
}

# Define competitors
competitors = ['boxboys', 'jawigrown2', 'dcweedevents_', 'dcweedeventsss', 'welit_dc_', 'welit18', 'welittogetherdc', 'highvoltage_71', 'weedwookie', 'knightkingdelivery_dc']

total_followers_added=0
# Main loop
i = 7500
while True:
    if i >= 50000:
        break

    # Switch between users for each iteration
    username = 'computertechservice1'
    password = user_credentials[username]
    session = os.path.join('/app', 'data', f'session-{username}')

    followers = []
    try:
        with instaloader.Instaloader() as L:
            L.load_session_from_file(username, session)
            profile = instaloader.Profile.from_username(L.context, competitors[-2])
            followers = get_followers_with_retry(profile, start_index=i, max_followers=1000, max_retries=3, delay_between_retries=60*20)
    except Exception as e:
        print(f"Error occurred during loading session or fetching followers: {e}")
        
    if len(followers) > 0:
        try:
            write_followers_to_csv(followers)
            print(f'{len(followers)} followers added.')
            total_followers_added+=len(followers)
        except Exception as e:
            print(f"Error occurred during writing to CSV: {e}")

    i += 1000
    time.sleep(60*15, 60*40)

print(f'Total {len(followers)} followers added to the followers list.')



