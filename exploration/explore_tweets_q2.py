#!/usr/bin/env python
"""explore_tweets_q2.py

Script to explore tweet fields relevant for Q2: finding the most used emojis.
Counts how often the content field appears, its type, and collects sample texts.
"""

import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parent.parent / "src").resolve()))

import json
import logging
from collections import Counter
from google.cloud import storage
from google.cloud.exceptions import NotFound
from utils import get_config_value

EXAMPLES_LIMIT = 20


def open_gcs_file(bucket_name: str, filename: str):
    client = storage.Client()
    gcs_bucket = client.bucket(bucket_name)
    blob = gcs_bucket.blob(filename)
    return blob.open("rt")


def explore_tweets_content(
    tweets_file_path: str, max_lines: int = 200_000, log_file: str = None
) -> None:
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")
    log = logging.info if log_file else print

    field_counter = Counter()
    missing_content = 0
    content_type_counter = Counter()
    malformed_lines = 0
    example_contents = set()
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

            tweet_content = tweet.get("content") or tweet.get("renderedContent")
            if tweet_content is None:
                missing_content += 1
            else:
                content_type_counter[type(tweet_content).__name__] += 1
                if len(example_contents) < EXAMPLES_LIMIT:
                    example_contents.add(tweet_content)

    log(f"Total lines analyzed: {lines_analyzed}")
    log(f"Malformed lines: {malformed_lines}")
    log(f"Field freq (top 20): {field_counter.most_common(20)}")
    log(f"Content field type counts: {content_type_counter}")
    log(f"Lines missing content: {missing_content}")
    log(f"Example tweet contents ({len(example_contents)}):")
    for example in example_contents:
        log(example)


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    bucket = get_config_value("BUCKET")
    filename = get_config_value("FILENAME")
    file_path = f"gs://{bucket}/{filename}"
    explore_tweets_content(
        tweets_file_path=file_path,
        max_lines=200_000,
        log_file=str(current_dir / "tweet_explore_q2.log"),
    )
