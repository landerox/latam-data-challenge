"""
Module for finding the top N most used emojis in tweets.
Optimized for low memory usage by processing the file line by line.
"""

from typing import List, Tuple
import json
import re
from collections import Counter

from utils import get_local_file_path


def q2_memory(file_path: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Finds the top N most used emojis in all tweets (memory-efficient).

    Args:
        file_path: Path to the tweets file (JSON lines format).
        top_n: Number of top emojis to return (default is 10).

    Returns:
        List of tuples: (emoji, count).
    """
    file_path = get_local_file_path(file_path)
    emoji_counter = Counter()

    # Changed: removed "+" so each emoji is matched individually.
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\U00002700-\U000027bf"
        "\U000024c2-\U0001f251"
        "]",
        flags=re.UNICODE,
    )

    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
                content = tweet_data.get("content")
                if not content:
                    continue
                emojis_found = emoji_pattern.findall(content)
                emoji_counter.update(emojis_found)
            except json.JSONDecodeError:
                continue

    return emoji_counter.most_common(top_n)
