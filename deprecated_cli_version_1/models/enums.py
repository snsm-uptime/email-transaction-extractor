from enum import Enum, auto


class Bank(Enum):
    PROMERICA = "info@promerica.fi.cr"
    BAC = "notificacion@notificacionesbaccr.com"
    SIMAN = ""


class ExpensePriority(Enum):
    MUST = auto()
    WANT = auto()
    NEED = auto()


class ExpenseType(Enum):
    TAXES = auto()
    GROCERIES = auto()
    EATING_OUT = auto()
    ENTERTAINMENT = auto()
    TRANSPORT = auto()
    SELF_CARE = auto()
    PET = auto()
    GIFT = auto()


class ImapServer(Enum):
    GOOGLE = 'imap.gmail.com'
    OUTLOOK = 'imap-mail.outlook.com'
    YAHOO = 'imap.mail.yahoo.com'
    CUSTOM = 'custom'


class OutputFormat(Enum):
    JSON = 'json'
    CSV = 'csv'


class StorageType(Enum):
    FILE = 'file'
    SQLITE = 'sqlite'
    POSTGRES = 'postgres'
