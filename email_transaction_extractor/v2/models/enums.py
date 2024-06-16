from enum import Enum


class OutputFormat(Enum):
    JSON = 'json'
    CSV = 'csv'


class StorageType(Enum):
    FILE = 'file'
    DATABASE = 'database'


class ImapServer(Enum):
    GOOGLE = 'google'
    OUTLOOK = 'outlook'
    YAHOO = 'yahoo'
    CUSTOM = 'custom'
