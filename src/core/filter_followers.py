"""
Module for filtering and deduplicating Instagram follower data from CSV files.
Handles the removal of duplicate usernames while preserving data integrity.
"""

import csv
from pathlib import Path
from typing import Set, Dict, Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class CSVPaths:
    """Store CSV file paths configuration."""
    input_path: Path
    output_path: Optional[Path] = None

    def __post_init__(self):
        """Ensure output path exists, default to input path if not specified."""
        if self.output_path is None:
            self.output_path = self.input_path

class FollowerDataCleaner:
    """Handles the cleaning and deduplication of follower data from CSV files."""

    def __init__(self, file_paths: CSVPaths):
        """
        Initialize the FollowerDataCleaner with file paths.

        Args:
            file_paths: CSVPaths object containing input and output file paths
        """
        self.file_paths = file_paths
        self.unique_usernames: Set[str] = set()

    def read_and_deduplicate(self) -> None:
        """Read CSV file and collect unique usernames."""
        try:
            with open(self.file_paths.input_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if 'username' not in reader.fieldnames:
                    raise ValueError("CSV file must contain 'username' column")
                
                for row in reader:
                    username = row['username'].strip()
                    if username:  # Only add non-empty usernames
                        self.unique_usernames.add(username)
                        
            logger.info(f"Found {len(self.unique_usernames)} unique usernames")
            
        except FileNotFoundError:
            logger.error(f"Input file not found: {self.file_paths.input_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise

    def save_unique_usernames(self) -> None:
        """Save deduplicated usernames back to CSV file."""
        try:
            with open(self.file_paths.output_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['username'])
                writer.writeheader()
                
                for username in sorted(self.unique_usernames):  # Sort for consistent output
                    writer.writerow({'username': username})
                    
            logger.info(f"Successfully saved {len(self.unique_usernames)} "
                       f"unique usernames to {self.file_paths.output_path}")
            
        except Exception as e:
            logger.error(f"Error writing to CSV file: {e}")
            raise

    def process(self) -> None:
        """Execute the complete deduplication process."""
        try:
            self.read_and_deduplicate()
            self.save_unique_usernames()
        except Exception as e:
            logger.error(f"Failed to process followers: {e}")
            raise

class FollowerStats:
    """Provides statistical analysis of follower data."""

    @staticmethod
    def get_duplicate_count(file_path: Path) -> Dict[str, int]:
        """
        Calculate the number of duplicates in the original file.

        Args:
            file_path: Path to the CSV file

        Returns:
            Dictionary with username counts
        """
        username_counts: Dict[str, int] = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    username = row['username'].strip()
                    if username:
                        username_counts[username] = username_counts.get(username, 0) + 1
                        
            return {k: v for k, v in username_counts.items() if v > 1}
            
        except Exception as e:
            logger.error(f"Error calculating duplicate statistics: {e}")
            raise

def main():
    """Main execution function."""
    try:
        # Configure file paths
        file_paths = CSVPaths(
            input_path=Path('../../data/followers_insta.csv')
        )

        # Initialize and run the cleaner
        cleaner = FollowerDataCleaner(file_paths)
        
        # Optional: Get duplicate statistics before cleaning
        stats = FollowerStats()
        duplicates = stats.get_duplicate_count(file_paths.input_path)
        if duplicates:
            logger.info(f"Found {len(duplicates)} usernames with duplicates")
            
        # Process the data
        cleaner.process()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()
