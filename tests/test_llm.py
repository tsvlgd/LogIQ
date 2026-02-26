from llm_service import LLMService

def test_llm():
    llm = LLMService()
    
    test_logs = [
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active.",
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025",
        "System reboot initiated by user 12345.",
        "404 Not Found: The requested resource was not found on this server.",
        "CPU usage exceeded 90% threshold for process ID 8923.",
        "Failed to escalate workflow: Invalid transition from 'pending' to 'resolved'."
    ]

    for log in test_logs:
        label = llm.classify(log)
        print("Log:", log)
        print("Predicted:", label)
        print("-" * 60)

if __name__ == "__main__":
    test_llm()