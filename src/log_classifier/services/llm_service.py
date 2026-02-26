from dotenv.main import load_dotenv
from groq import Groq
import re
import os
from dotenv import load_dotenv

load_dotenv()


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
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def classify(self, log_message: str, model_name: str = "llama-3.1-8b-instant") -> str:

        system_prompt = """
You are a strict log classification engine.

You must classify the log into EXACTLY ONE of:

- Critical Error
- Error
- HTTP Status
- Resource Usage
- Security Alert
- Workflow Error
- Deprecation Warning
- System Notification
- User Action

Classification guidelines:

- If message contains HTTP codes (404, 500, etc.) → HTTP Status
- If message mentions CPU, memory, disk, usage → Resource Usage
- If message mentions unauthorized access, login failures → Security Alert
- If message mentions workflow, escalation, invalid transitions → Workflow Error
- If message mentions deprecated, retired, no longer supported → Deprecation Warning
- If message describes reboot, backup, update success → System Notification
- If message describes user login/logout or account creation → User Action
- If message indicates system crash or major failure → Critical Error
- If message indicates generic failure → Error
"""
        messages = [
        {"role":"system", "content": system_prompt},
        {"role":"user", "content": log_message}
    ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.0
        )

        content = response.choices[0].message.content
        return content