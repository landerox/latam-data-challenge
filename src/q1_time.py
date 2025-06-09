"""q1_time.

Module for finding the top N dates with the most tweets and the most active user
for each of those dates. Optimized for execution speed using pandas.
"""

from typing import List, Tuple
from datetime import date
import json
import pandas as pd

from utils import get_local_file_path


def q1_time(file_path: str, top_n: int = 10) -> List[Tuple[date, str]]:
    """
    Computes the top N days with the highest tweet volume and, for each day, the user
    with the most tweets. Uses pandas for efficient in-memory aggregation.
    Handles malformed or incomplete records gracefully.

    Args:
        file_path: Path to the tweets file (JSON lines format).
        top_n: Number of top dates to return (default is 10).

    Returns:
        List of tuples: (date, username_with_highest_activity_that_day).
    """
    file_path = get_local_file_path(file_path)
    tweet_records = []

    with open(file_path, encoding="utf-8") as infile:
        for raw_line in infile:
            try:
                tweet_data = json.loads(raw_line)
                tweet_date_str = tweet_data.get("date")
                user_data = tweet_data.get("user", {})
                username = user_data.get("username")
                if tweet_date_str and username:
                    tweet_records.append({"date": tweet_date_str, "username": username})
            except json.JSONDecodeError:
                continue

    if not tweet_records:
        return []

    df_tweets = pd.DataFrame(tweet_records)
    df_tweets["date"] = pd.to_datetime(df_tweets["date"], errors="coerce").dt.date
    df_tweets = df_tweets.dropna(subset=["date", "username"])

    user_activity = (
        df_tweets.groupby(["date", "username"]).size().reset_index(name="tweet_count")
    )

    daily_totals = (
        user_activity.groupby("date")["tweet_count"]
        .sum()
        .reset_index()
        .sort_values("tweet_count", ascending=False)
        .head(top_n)
    )

    result = []
    for _, top_day in daily_totals.iterrows():
        current_date = top_day["date"]
        users_on_day = user_activity[user_activity["date"] == current_date]
        most_active_user = users_on_day.sort_values(
            "tweet_count", ascending=False
        ).iloc[0]
        result.append((current_date, most_active_user["username"]))

    return result
