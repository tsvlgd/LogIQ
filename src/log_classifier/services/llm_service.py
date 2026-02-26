from log_classifier.config import settings
from groq import Groq
import re
import os


VALID_LABELS = {
    "Critical Error",
    "Error",
    "HTTP Status",
    "Resource Usage",
    "Security Alert",
    "Workflow Error",
    "Deprecation Warning",
    "System Notification",
    "User Action",
}


class LLMService:
    def __init__(self):
        api_key = settings.groq_api_key
        self.client = Groq(api_key=api_key)

    def classify(
        self,
        log_message: str,
        model_name: str = "llama-3.1-8b-instant",
    ) -> str:

        system_prompt = """
        You are a deterministic log classification engine.

        Your task is to assign the given log message to EXACTLY ONE label from the list below.

        You MUST follow these rules strictly:
        - Output ONLY one label.
        - Do NOT explain your reasoning.
        - Do NOT add extra words.
        - Do NOT add punctuation.
        - Do NOT return multiple labels.
        - Do NOT include formatting or newlines.
        - Return the label exactly as written.

        Valid labels:

        Critical Error
        Error
        HTTP Status
        Resource Usage
        Security Alert
        Workflow Error
        Deprecation Warning
        System Notification
        User Action

    Classification rules:

        - Logs containing HTTP status codes (e.g., 404, 500) → HTTP Status
        - Logs mentioning CPU, memory, disk, or resource thresholds → Resource Usage
        - Logs mentioning unauthorized access, login failures, privilege misuse → Security Alert
        - Logs involving workflow transitions, escalation failures, invalid state changes → Workflow Error
        - Logs mentioning deprecated, retired, unsupported components → Deprecation Warning
        - Logs describing reboot, backup, successful updates, normal operations → System Notification
        - Logs describing user login, logout, or account activity → User Action
        - Logs describing crashes, corruption, catastrophic failure, or service halt → Critical Error
        - All other failures or generic issues → Error

    If uncertain, choose the single most appropriate label.
    """.strip()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": log_message},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.0,
        )
        
        content = response.choices[0].message.content.strip()

        if content in VALID_LABELS:
            return content

        # Attempt extraction
        for label in VALID_LABELS:
            if label in content:
                return label

        return "Error"