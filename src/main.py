"""main.py

Entrypoint script to run data challenge Q solutions from the command line.
Uses argparse for parameters and logging for output.
"""

import argparse
import logging
from typing import NoReturn

from q1_memory import q1_memory
from q1_time import q1_time
from q2_memory import q2_memory
from q2_time import q2_time
from q3_memory import q3_memory
from q3_time import q3_time
from utils import get_config_value

logging.basicConfig(level=logging.INFO)


def run_q1(file_path: str, method: str, top_n: int) -> None:
    """Run Q1 (time or memory) and log the result."""
    logging.info("Running Q1 | Method: %s | Top N: %d", method, top_n)
    if method == "time":
        result = q1_time(file_path, top_n=top_n)
    else:
        result = q1_memory(file_path, top_n=top_n)
    logging.info("Q1 Result: %s", result)


def run_q2(file_path: str, method: str, top_n: int) -> None:
    """Run Q2 (time or memory) and log the result."""
    logging.info("Running Q2 | Method: %s | Top N: %d", method, top_n)
    if method == "time":
        result = q2_time(file_path, top_n=top_n)
    else:
        result = q2_memory(file_path, top_n=top_n)
    logging.info("Q2 Result: %s", result)


def run_q3(file_path: str, method: str, top_n: int) -> None:
    """Run Q3 (time or memory) and log the result."""
    logging.info("Running Q3 | Method: %s | Top N: %d", method, top_n)
    if method == "time":
        result = q3_time(file_path, top_n=top_n)
    else:
        result = q3_memory(file_path, top_n=top_n)
    logging.info("Q3 Result: %s", result)


def main() -> NoReturn:
    """
    Runs the selected Q solution with the given parameters.

    Parses arguments, loads config, selects method/question, logs the results.
    """
    parser = argparse.ArgumentParser(description="Run data challenge Q solutions.")
    parser.add_argument(
        "--question",
        choices=["q1", "q2", "q3"],
        default="q1",
        help="Which question to solve: 'q1', 'q2', or 'q3'.",
    )
    parser.add_argument(
        "--method",
        choices=["time", "memory"],
        default="time",
        help="Method: 'time' (fast, pandas) or 'memory' (low RAM).",
    )
    parser.add_argument(
        "--top_n", type=int, default=10, help="Number of top results to return."
    )
    args = parser.parse_args()

    bucket = get_config_value("BUCKET")
    filename = get_config_value("FILENAME")
    file_path = f"gs://{bucket}/{filename}"

    logging.info("Using file: %s", file_path)
    logging.info(
        "Question: %s | Method: %s | Top N: %d", args.question, args.method, args.top_n
    )

    if args.question == "q1":
        run_q1(file_path, args.method, args.top_n)
    elif args.question == "q2":
        run_q2(file_path, args.method, args.top_n)
    elif args.question == "q3":
        run_q3(file_path, args.method, args.top_n)


if __name__ == "__main__":
    main()
