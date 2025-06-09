#!/usr/bin/env python
"""explore_tweets_q3.py

Script to explore mention fields relevant for Q3: finding most mentioned users.
Counts mention-related fields, types, and collects sample mention objects.
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


def explore_mentions(
    tweets_file_path: str, max_lines: int = 200_000, log_file: str = None
) -> None:
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")
    log = logging.info if log_file else print

    field_counter = Counter()
    mention_field_type_counter = Counter()
    example_mentions = set()
    malformed_lines = 0
    lines_analyzed = 0
    missing_mentions = 0

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

            mentioned = tweet.get("mentionedUsers")
            if mentioned is None and "entities" in tweet:
                entities = tweet.get("entities", {})
                mentioned = entities.get("mentions")
            if mentioned is None:
                missing_mentions += 1
            else:
                mention_field_type_counter[type(mentioned).__name__] += 1
                if len(example_mentions) < EXAMPLES_LIMIT:
                    example_mentions.add(str(mentioned))

    log(f"Total lines analyzed: {lines_analyzed}")
    log(f"Malformed lines: {malformed_lines}")
    log(f"Field freq (top 20): {field_counter.most_common(20)}")
    log(f"Mention field type counts: {mention_field_type_counter}")
    log(f"Lines missing mention info: {missing_mentions}")
    log(f"Example mention objects ({len(example_mentions)}):")
    for example in example_mentions:
        log(example)


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    bucket = get_config_value("BUCKET")
    filename = get_config_value("FILENAME")
    file_path = f"gs://{bucket}/{filename}"
    explore_mentions(
        tweets_file_path=file_path,
        max_lines=200_000,
        log_file=str(current_dir / "tweet_explore_q3.log"),
    )
