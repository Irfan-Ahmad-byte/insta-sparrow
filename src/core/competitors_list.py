"""
Module for managing Instagram competitor analysis and follower extraction.
Handles follower retrieval and ghost follower filtering.
"""

import time
import csv
import random
from typing import Set, List, Iterator, Optional
from pathlib import Path
from itertools import islice, chain

import instaloader
from instaloader.structures import Profile, User

# Constants
DATA_DIR = Path('../../data')
OUTPUT_FILE = DATA_DIR / 'followers_insta.csv'
RESUME_FILE = DATA_DIR / 'resume_information.json'

class CompetitorAnalyzer:
    def __init__(self, username: str, session_name: str = None):
        """
        Initialize CompetitorAnalyzer with Instagram credentials.
        
        Args:
            username: Instagram username for authentication
            session_name: Optional session name, defaults to f'session-{username}'
        """
        self.username = username
        self.session_name = session_name or f'session-{username}'
        self.loader = instaloader.Instaloader()
        
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def authenticate(self) -> None:
        """Authenticate with Instagram using saved session."""
        try:
            self.loader.load_session_from_file(self.username, self.session_name)
        except Exception as e:
            raise ConnectionError(f"Failed to authenticate: {str(e)}")

    @staticmethod
    def clean_ghost_followers(profile: Profile, followers: Set[User]) -> Set[User]:
        """
        Filter out ghost followers by checking post engagement.
        
        Args:
            profile: Instagram profile to analyze
            followers: Set of followers to clean
            
        Returns:
            Set of active followers who have liked posts
        """
        likes = set()
        for post in profile.get_posts():
            likes.update(post.get_likes())
        
        return followers.intersection(likes)

    def get_followers(self, usernames: List[str]) -> Iterator[User]:
        """
        Retrieve and clean followers from multiple competitor accounts.
        
        Args:
            usernames: List of competitor usernames to analyze
            
        Returns:
            Iterator of cleaned followers
        """
        cleaned_followers = []
        
        for username in usernames:
            try:
                profile = instaloader.Profile.from_username(self.loader.context, username)
                followers = set(profile.get_followers())
                active_followers = self.clean_ghost_followers(profile, followers)
                cleaned_followers = chain(cleaned_followers, active_followers)
                
            except Exception as e:
                print(f'Error processing {username}: {str(e)}')
                
        return cleaned_followers

    def get_followers_with_retry(
        self,
        followers_iterator: Iterator[User],
        start_index: int = 0,
        max_followers: Optional[int] = 400,
        max_retries: int = 3,
        delay_between_retries: int = 1200  # 20 minutes in seconds
    ) -> List[List[str]]:
        """
        Retrieve followers with retry mechanism for handling rate limits.
        
        Args:
            followers_iterator: Iterator of followers
            start_index: Starting index for slicing followers
            max_followers: Maximum number of followers to retrieve
            max_retries: Maximum number of retry attempts
            delay_between_retries: Delay between retries in seconds
            
        Returns:
            List of follower usernames
        """
        followers = []
        retries = 0
        
        while retries < max_retries:
            try:
                if max_followers is not None:
                    end_index = start_index + max_followers
                    followers_slice = islice(followers_iterator, start_index, end_index)
                else:
                    followers_slice = islice(followers_iterator, start_index, None)
                
                for follower in followers_slice:
                    try:
                        followers.append([follower.username])
                    except Exception as e:
                        print(f"Error processing follower: {str(e)}")
                        self._save_progress(followers_iterator)
                        return followers

                return followers
                
            except instaloader.exceptions.QueryReturnedBadRequestException:
                retries += 1
                if retries < max_retries:
                    print(f"Rate limit hit, retrying... ({retries}/{max_retries})")
                    time.sleep(delay_between_retries)
                else:
                    print("Max retries reached. Stopping.")
                    
        return followers

    def _save_progress(self, followers_iterator: Iterator[User]) -> None:
        """Save current progress to resume later."""
        try:
            instaloader.save(str(RESUME_FILE), followers_iterator.freeze())
        except Exception as e:
            print(f"Failed to save progress: {str(e)}")

    def process_competitors(
        self,
        competitors: List[str],
        batch_size: int = 500,
        min_delay_hours: float = 36,  # 1.5 days
        max_delay_hours: float = 60   # 2.5 days
    ) -> None:
        """
        Process competitor accounts and save their followers.
        
        Args:
            competitors: List of competitor usernames
            batch_size: Number of followers to process in each batch
            min_delay_hours: Minimum delay between batches in hours
            max_delay_hours: Maximum delay between batches in hours
        """
        try:
            cleaned_followers = self.get_followers(competitors)
            total_followers = list(cleaned_followers)
            batch_count = len(total_followers) // batch_size
            
            for i in range(batch_count):
                if i == batch_count - 1:
                    break
                    
                followers = self.get_followers_with_retry(
                    cleaned_followers,
                    start_index=batch_size * i,
                    max_followers=batch_size
                )
                
                if followers:
                    self._save_batch_to_csv(followers)
                    print(f'Added {len(followers)} followers')
                
                # Random delay between batches
                delay_seconds = random.uniform(
                    min_delay_hours * 3600,
                    max_delay_hours * 3600
                )
                time.sleep(delay_seconds)
                
        except Exception as e:
            print(f"Error processing competitors: {str(e)}")

    def _save_batch_to_csv(self, followers: List[List[str]]) -> None:
        """Save a batch of followers to CSV file."""
        with open(OUTPUT_FILE, 'a', newline='') as fl:
            writer = csv.writer(fl)
            writer.writerows(followers)

def main():
    """Main execution function."""
    # Example competitor usernames
    competitors = ["competitor1", "competitor2", "competitor3"]
    
    # Initialize analyzer
    analyzer = CompetitorAnalyzer(username="your_username")
    
    # Authenticate and process competitors
    analyzer.authenticate()
    analyzer.process_competitors(competitors)

if __name__ == "__main__":
    main()
