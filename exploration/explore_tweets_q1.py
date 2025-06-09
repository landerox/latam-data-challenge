#!/usr/bin/env python
"""explore_tweets_q1.py

Script to explore tweet fields relevant for Q1: finding the top N dates with the
most tweets and the most active user per date.
Counts how often the date and user fields appear, their types, and collects sample
values to assist in data validation and edge case detection.
"""

import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parent.parent / "src").resolve()))

import json
import logging
from collections import Counter

from dateutil import parser as dtparser
from google.cloud import storage
from google.cloud.exceptions import NotFound

from utils import get_config_value

EXAMPLES_LIMIT = 1000
BAD_DATE_LIMIT = 100


def open_gcs_file(bucket_name: str, filename: str):
    client = storage.Client()
    gcs_bucket = client.bucket(bucket_name)
    blob = gcs_bucket.blob(filename)
    return blob.open("rt")


def explore_tweets(
    tweets_file_path: str, max_lines: int = 200_000, log_file: str = None
) -> None:
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")
    log = logging.info if log_file else print

    field_counter = Counter()
    created_at_formats = Counter()
    missing_user = 0
    missing_screen_name = 0
    malformed_lines = 0
    example_dates = set()
    bad_date_examples = set()
    lines_analyzed = 0

    if tweets_file_path.startswith("gs://"):
        try:
            path = tweets_file_path.replace("gs://", "")
            bucket_name, gcs_filename = path.split("/", 1)
            f = open_gcs_file(bucket_name, gcs_filename)
        except NotFound as e:
            log(f"File not found in GCS: {e}")
            return
        except (OSError, IOError) as e:
            log(f"Failed to open file from GCS: {e}")
            return
    else:
        try:
            f = open(tweets_file_path, encoding="utf-8")
        except (OSError, IOError) as e:
            log(f"Failed to open local file: {e}")
            return

    with f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            lines_analyzed += 1
            try:
                tweet = json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
                continue
            for key in tweet:
                field_counter[key] += 1

            created_at = tweet.get("created_at")
            if created_at:
                try:
                    dt = dtparser.parse(created_at)
                    fmt = dt.strftime("%a %b %d %H:%M:%S %z %Y")
                    created_at_formats[fmt] += 1
                    if len(example_dates) < EXAMPLES_LIMIT:
                        example_dates.add(created_at)
                except (ValueError, TypeError):
                    created_at_formats["unparseable"] += 1
                    if len(bad_date_examples) < BAD_DATE_LIMIT:
                        bad_date_examples.add(created_at)

            user = tweet.get("user")
            if not user:
                missing_user += 1
            else:
                screen_name = user.get("screen_name")
                if not screen_name:
                    missing_screen_name += 1

    log(f"Total lines analyzed: {lines_analyzed}")
    log(f"Malformed lines: {malformed_lines}")
    log(f"Field freq (top 20): {field_counter.most_common(20)}")
    log(f"created_at format freq: {created_at_formats}")
    log(f"Unique created_at examples ({len(example_dates)}): {list(example_dates)}")
    log(
        f"Bad created_at examples ({len(bad_date_examples)}): {list(bad_date_examples)}"
    )
    log(f"Lines missing user: {missing_user}")
    log(f"Lines missing screen_name: {missing_screen_name}")


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    bucket = get_config_value("BUCKET")
    filename = get_config_value("FILENAME")
    file_path = f"gs://{bucket}/{filename}"
    explore_tweets(
        tweets_file_path=file_path,
        max_lines=200_000,
        log_file=str(current_dir / "tweet_explore_q1.log"),
    )
