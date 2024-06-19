from abc import ABC
from email.header import decode_header
from email.message import Message

from bs4 import BeautifulSoup

from ..email.processing import extract_email_from_string


class Mail(ABC):
    def __init__(self, msg: Message):
        decoded_header = decode_header(msg.get('subject'))

        normalized_subject = ""
        for part, encoding in decoded_header:
            if isinstance(part, bytes):
                if encoding is None or encoding == 'unknown-8bit':
                    encoding = "utf-8"
                normalized_subject += part.decode(encoding, errors="replace")
            else:
                normalized_subject += part

        self.msg = msg
        self.subject = normalized_subject
        self.author = extract_email_from_string(msg.get('from'))
        self.body = self.__get_body(msg)
        self.date = msg.get('date')

    def __get_body(self, msg: Message):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True)
                        charset = part.get_content_charset()
                        if charset is None:
                            charset = "utf-8"
                        body = body.decode(charset, errors="replace")
                        if content_type == "text/plain":
                            return body
                        elif content_type == "text/html":
                            soup = BeautifulSoup(body, "html.parser")
                            return soup.find('body').get_text()
                    except:
                        pass
        else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if charset is None:
                charset = "utf-8"
            body = body.decode(charset, errors="replace")
            if content_type == "text/plain":
                return body
            elif content_type == "text/html":
                soup = BeautifulSoup(body, "html.parser")
                return soup.get_text()
        return ""

    def __str__(self):
        return f"Subject: {self.subject}\nRecipient: {self.authors}\nDate: {self.date}\nBody: {self.body}\n"
