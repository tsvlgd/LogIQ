import re
from typing import Optional


class RegexService:
    def __init__(self):
        self.patterns = {
            r"User User\d+ logged (in|out).": "User Action",
            r"Backup (started|ended) at .*": "System Notification",
            r"Backup completed successfully.": "System Notification",
            r"System updated to version .*": "System Notification",
            r"File .* uploaded successfully by user .*": "System Notification",
            r"Disk cleanup completed successfully.": "System Notification",
            r"System reboot initiated by user .*": "System Notification",
            r"Account with ID .* created by .*": "User Action"
        }

    def classify(self, text: str) -> Optional[str]:
        for pattern, label in self.patterns.items():
            if re.search(pattern, text):
                return label
        return None