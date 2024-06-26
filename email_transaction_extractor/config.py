from dotenv import load_dotenv
from .models.enums import ImapServer
from os import getenv

load_dotenv()

EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
EMAIL_USER = getenv('EMAIL_USER')
EMAIL_SERVER = ImapServer.GOOGLE.value
EMAIL_MAILBOX = "inbox"
