from datetime import datetime, timezone

def batch_time():
    return datetime.now(timezone.utc).isoformat()