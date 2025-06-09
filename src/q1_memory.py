"""q1_memory.

Module for finding the top N dates with the most tweets and the most active user
for each of those dates. Optimized for low memory usage by processing the file line by line.
"""

from typing import List, Tuple
from datetime import date, datetime
import json


def q1_memory(file_path: str, top_n: int = 10) -> List[Tuple[date, str]]:
    """
    Finds the top N dates with the most tweets and, for each date, the user
    with the highest tweet count. Processes file line by line for minimal memory usage.

    Args:
        file_path: Path to the tweets file (JSON lines format, local or cloud).
        top_n: Number of top dates to return (default is 10).

    Returns:
        A list of tuples: (date, username_with_most_tweets_on_that_date).
    """
    # Dictionary to count tweets per user per date
    tweet_volume_by_date_user = {}
    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
            except json.JSONDecodeError:
                continue  # Skip malformed JSON lines

            tweet_date_str = tweet_data.get("date")
            user_data = tweet_data.get("user")
            if not tweet_date_str or not user_data:
                continue  # Skip if date or user is missing

            username = user_data.get("username")
            if not username:
                continue  # Skip if username is missing

            try:
                tweet_date = datetime.fromisoformat(
                    tweet_date_str.replace("Z", "+00:00")
                ).date()
            except (ValueError, TypeError):
                continue  # Skip if date parsing fails

            if tweet_date not in tweet_volume_by_date_user:
                tweet_volume_by_date_user[tweet_date] = {}
            user_volume_map = tweet_volume_by_date_user[tweet_date]
            user_volume_map[username] = user_volume_map.get(username, 0) + 1

    # Sort dates by total tweet count and get top N
    top_dates = sorted(
        tweet_volume_by_date_user.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True,
    )[:top_n]

    # For each top date, find the user with the most tweets
    result = []
    for tweet_date, user_counts in top_dates:
        top_user = max(user_counts.items(), key=lambda x: x[1])[0]
        result.append((tweet_date, top_user))
    return result
