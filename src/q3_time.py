"""q3_time.

Module for finding the top N most mentioned usernames in all tweets.
Optimized for execution speed using pandas.
"""

from typing import List, Tuple
import json
import pandas as pd


def q3_time(file_path: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Finds the top N usernames most frequently mentioned in all tweets.

    Args:
        file_path: Path to the tweets file (JSON lines format).
        top_n: Number of top mentioned usernames to return (default is 10).

    Returns:
        List of tuples: (username, mention_count).
    """
    mention_lists = []
    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
                mentioned = tweet_data.get("mentionedUsers")
                if isinstance(mentioned, list):
                    # Extract usernames for each mention
                    usernames = [
                        user.get("username")
                        for user in mentioned
                        if user.get("username")
                    ]
                    mention_lists.extend(usernames)
            except json.JSONDecodeError:
                continue

    if not mention_lists:
        return []

    # Use pandas Series for fast counting
    mention_series = pd.Series(mention_lists)
    mention_counts = mention_series.value_counts().head(top_n)
    return list(mention_counts.items())
