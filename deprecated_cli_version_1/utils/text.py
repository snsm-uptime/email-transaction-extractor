import re


def extract_email_from_string(text: str) -> str | None:
    # Regular expression to extract email address
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if match:
        return match.group(0)
    return None
