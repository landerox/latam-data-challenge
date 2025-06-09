"""utils.py

Module provides configuration retrieval and BigQuery helper functions.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple
from zoneinfo import ZoneInfo

from google.cloud import bigquery, storage
import tempfile


def get_config_value(key: str) -> str:
    """Retrieve a value from the config.json file by key.

    Args:
        key: The name of the config key to retrieve.

    Returns:
        The corresponding value as a string, or an empty string
        if the key is not found or an error occurs.
    """
    config_path = Path(__file__).resolve().parent / "config.json"
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get(key, "")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ""


def save_results_to_bq(
    result: List[Tuple[Any, ...]],
    question: str,
    method: str,
    project_id: str,
    dataset_id: str,
) -> None:
    """
    Save results to the corresponding BigQuery table, adding 'method' and 'ingested_at'.

    Args:
        result: List of tuples (output from Q functions)
        question: "q1", "q2", or "q3"
        method: "time" or "memory"
        project_id: GCP project ID
        dataset_id: BigQuery dataset ID
    """
    table_map = {"q1": "q1_results", "q2": "q2_results", "q3": "q3_results"}
    table_id = f"{project_id}.{dataset_id}.{table_map[question]}"
    client = bigquery.Client(project=project_id)

    # Use America/Santiago timezone for ingestion timestamp
    ingested_at = datetime.now(ZoneInfo("America/Santiago")).isoformat()

    # Prepare rows to insert based on question type
    rows_to_insert: List[Dict[str, Any]] = []
    if question == "q1":
        for row in result:
            rows_to_insert.append(
                {
                    "tweet_date": str(row[0]),
                    "top_user": row[1],
                    "method": method,
                    "ingested_at": ingested_at,
                }
            )
    elif question == "q2":
        for row in result:
            rows_to_insert.append(
                {
                    "emoji": row[0],
                    "count": row[1],
                    "method": method,
                    "ingested_at": ingested_at,
                }
            )
    elif question == "q3":
        for row in result:
            rows_to_insert.append(
                {
                    "username": row[0],
                    "mention_count": row[1],
                    "method": method,
                    "ingested_at": ingested_at,
                }
            )

    # Truncate table before inserting new results
    client.query(f"DELETE FROM `{table_id}` WHERE TRUE").result()  # nosec

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        logging.error("Failed to insert into BigQuery: %s", errors)
    else:
        logging.info("Results saved to BigQuery table: %s", table_id)


def get_local_file_path(file_path: str) -> str:
    """
    Downloads a file from GCS if `file_path` starts with 'gs://',
    saves it to a temporary location using pathlib, and returns the local path.

    Args:
        file_path: Path to the file (GCS URI or local path).

    Returns:
        Path to a local file as string.
    """
    if file_path.startswith("gs://"):
        bucket_name, blob_path = file_path[5:].split("/", 1)
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        temp_dir = Path(tempfile.gettempdir())
        local_path = temp_dir / Path(blob_path).name
        blob.download_to_filename(str(local_path))

        return str(local_path)

    return str(Path(file_path).resolve())
