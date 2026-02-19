from flask import current_app

def send_notification(to_email: str, subject: str, body: str) -> None:
    provider = current_app.config.get("NOTIFY_PROVIDER", "console")

    if provider == "console":
        print("\n=== NOTIFICATION ===")
        print("TO:", to_email)
        print("SUBJECT:", subject)
        print(body)
        print("====================\n")
        return

    # Stub for real provider (SendGrid, SES, etc.)
    raise NotImplementedError("Notification provider not configured.")
