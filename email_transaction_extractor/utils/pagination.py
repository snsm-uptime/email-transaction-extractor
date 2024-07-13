import base64
import json
from typing import Optional


def encode_cursor(page: int, page_size: int) -> str:
    cursor_data = {"page": page, "page_size": page_size}
    cursor_str = json.dumps(cursor_data)
    return base64.urlsafe_b64encode(cursor_str.encode()).decode()


def decode_cursor(cursor: str) -> Optional[dict]:
    try:
        cursor_str = base64.urlsafe_b64decode(cursor.encode()).decode()
        return json.loads(cursor_str)
    except Exception as e:
        print(f"Failed to decode cursor: {e}")
        return None
