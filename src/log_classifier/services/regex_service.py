import re
from typing import Optional


class RegexService:
    def __init__(self):
        self.patterns = [
            (re.compile(r"User (User\d+ )?logged (in|out)", re.IGNORECASE), "User Action"),
            (re.compile(r"Backup (started|ended) at .*", re.IGNORECASE), "System Notification"),
            (re.compile(r"Backup completed successfully", re.IGNORECASE), "System Notification"),
            (re.compile(r"System updated to version .*", re.IGNORECASE), "System Notification"),
            (re.compile(r"File .* uploaded successfully by user .*", re.IGNORECASE), "System Notification"),
            (re.compile(r"Disk cleanup completed successfully", re.IGNORECASE), "System Notification"),
            (re.compile(r"System reboot initiated by user .*", re.IGNORECASE), "System Notification"),
            (re.compile(r"Account with ID .* created by .*", re.IGNORECASE), "User Action"),
        ]

    def classify(self, text: str) -> Optional[str]:
        for pattern, label in self.patterns:
            if pattern.search(text):
                return label
        return None