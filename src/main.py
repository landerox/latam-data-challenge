"""main.py

Entrypoint script to run data challenge Q solutions from the command line.
Uses argparse for parameters and logging for output.
"""

import argparse
import logging
from typing import Any, List, Tuple

from q1_memory import q1_memory
from q1_time import q1_time
from q2_memory import q2_memory
from q2_time import q2_time
from q3_memory import q3_memory
from q3_time import q3_time
from utils import get_config_value, save_results_to_bq

logging.basicConfig(level=logging.INFO)


def get_result(
    question: str, method: str, file_path: str, top_n: int
) -> List[Tuple[Any, ...]]:
    """
    Execute the corresponding function and return the result list.

    Args:
        question: 'q1', 'q2', or 'q3'
        method: 'time' or 'memory'
        file_path: Path to the input file (GCS or local)
        top_n: Number of top results

    Returns:
        List of tuples with the result.
    """
    if question == "q1":
        return (
            q1_time(file_path, top_n)
            if method == "time"
            else q1_memory(file_path, top_n)
        )
    elif question == "q2":
        return (
            q2_time(file_path, top_n)
            if method == "time"
            else q2_memory(file_path, top_n)
        )
    elif question == "q3":
        return (
            q3_time(file_path, top_n)
            if method == "time"
            else q3_memory(file_path, top_n)
        )
    else:
        raise ValueError(f"Unknown question: {question}")


def main() -> None:
    """
    Runs the selected Q solution with the given parameters.

    Parses arguments, loads config, selects method/question, logs the results,
    and optionally saves results to BigQuery.
    """
    parser = argparse.ArgumentParser(description="Run data challenge Q solutions.")
    parser.add_argument(
        "--question",
        choices=["q1", "q2", "q3", "all"],
        default="q1",
        help="Which question to solve: 'q1', 'q2', 'q3', or 'all'.",
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
    parser.add_argument(
        "--save_bq", action="store_true", help="Save result to BigQuery table."
    )
    args = parser.parse_args()

    bucket = get_config_value("BUCKET")
    filename = get_config_value("FILENAME")
    project_id = get_config_value("PROJECT_ID")
    dataset_id = get_config_value("DATASET_ID")
    file_path = f"gs://{bucket}/{filename}"

    logging.info("Using file: %s", file_path)
    logging.info(
        "Question: %s | Method: %s | Top N: %d", args.question, args.method, args.top_n
    )

    if args.question == "all":
        for q in ["q1", "q2", "q3"]:
            for method in ["time", "memory"]:
                logging.info("Processing %s with method %s...", q, method)
                result = get_result(q, method, file_path, args.top_n)
                logging.info("Result: %s", result)

                if args.save_bq:
                    if not project_id or not dataset_id:
                        logging.error(
                            "PROJECT_ID or DATASET_ID missing in config.json."
                        )
                    else:
                        save_results_to_bq(
                            result=result,
                            question=q,
                            method=method,
                            project_id=project_id,
                            dataset_id=dataset_id,
                        )
        return

    # Execute and get the result for a single question
    result = get_result(args.question, args.method, file_path, args.top_n)
    logging.info("Result: %s", result)

    if args.save_bq:
        if not project_id or not dataset_id:
            logging.error("PROJECT_ID or DATASET_ID missing in config.json.")
        else:
            save_results_to_bq(
                result=result,
                question=args.question,
                method=args.method,
                project_id=project_id,
                dataset_id=dataset_id,
            )


if __name__ == "__main__":
    main()
