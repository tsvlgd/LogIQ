# log_classifier/api/utils.py
import re
from typing import List
from log_classifier.api.schemas import LogRequest

# Detect common timestamp formats at start of line
TIMESTAMP_REGEX = re.compile(
    r"""
    ^
    (
        \d{4}-\d{2}-\d{2}            # YYYY-MM-DD
        (?:[ T]\d{2}:\d{2}:\d{2}(?:,\d{3})?)?  # Optional time + millis
        |
        \d{1,2}/\d{1,2}/\d{4}       # MM/DD/YYYY
        (?:\s+\d{2}:\d{2}:\d{2})?
    )
    """,
    re.VERBOSE,
)


def norm(raw_input: str) -> List[LogRequest]:
    """
    Normalize raw input into a list of LogRequest objects.
    Handles both single log lines and multi-line log entries.
    """
    logs: List[LogRequest] = []

    if isinstance(raw_input, str):
        
        for line in raw_input.splitlines():
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            match = TIMESTAMP_REGEX.match(line)
            if not match:
                continue  # Skip lines that don't start with a timestamp

            message = line[match.end():].strip("-:;| ")  # Remove timestamp and common delimiters
            if message:
                logs.append(LogRequest(message=message))

        return logs
    

if __name__ == "__main__":
    # Example usage
    raw_log = """
    2024-06-01 12:00:00,123 - User User123 logged in.
    2024-06-01 12:05:00,456 - User User123 performed action A.
    2024-06-01 12:10:00,789 - User User
    """
    result = norm(raw_log)
    print(result)