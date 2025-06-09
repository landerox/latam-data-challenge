"""q2_time.

Module for finding the top N most used emojis in tweets.
Optimized for execution speed using pandas.
"""

import json
import re
from typing import List, Tuple

import pandas as pd

from utils import get_local_file_path


def q2_time(file_path: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Finds the top N most used emojis in all tweets (fast, loads all into memory).

    Args:
        file_path: Path to the tweets file (JSON lines format).
        top_n: Number of top emojis to return (default is 10).

    Returns:
        List of tuples: (emoji, count).
    """
    file_path = get_local_file_path(file_path)
    tweet_contents = []

    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
                content = tweet_data.get("content")
                if content:
                    tweet_contents.append(content)
            except json.JSONDecodeError:
                continue

    if not tweet_contents:
        return []

    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\U00002700-\U000027bf"
        "\U000024c2-\U0001f251"
        "]+",
        flags=re.UNICODE,
    )

    content_series = pd.Series(tweet_contents)
    all_emojis = content_series.str.findall(emoji_pattern).explode()
    emoji_counts = all_emojis.value_counts().head(top_n)
    return list(emoji_counts.items())
