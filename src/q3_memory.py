"""q3_memory.

Module for finding the top N most mentioned usernames in all tweets.
Optimized for low memory usage by processing the file line by line.
"""

from typing import List, Tuple
import json
from collections import Counter


def q3_memory(file_path: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Finds the top N usernames most frequently mentioned in all tweets.

    Args:
        file_path: Path to the tweets file (JSON lines format).
        top_n: Number of top mentioned usernames to return (default is 10).

    Returns:
        List of tuples: (username, mention_count).
    """
    mention_counter = Counter()
    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
                mentioned = tweet_data.get("mentionedUsers")
                if isinstance(mentioned, list):
                    for user in mentioned:
                        username = user.get("username")
                        if username:
                            mention_counter[username] += 1
            except json.JSONDecodeError:
                continue  # Skip malformed JSON lines

    return mention_counter.most_common(top_n)
