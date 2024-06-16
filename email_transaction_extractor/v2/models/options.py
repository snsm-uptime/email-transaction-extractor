from pydantic import BaseModel, Field
from typing import List, Optional

from .date import DateRange
from .enums import OutputFormat, StorageType, ImapServer


class CLIOptions(BaseModel):
    user: str = Field(..., description="Email account username")
    password: str = Field(..., description="Email account password")
    mailbox: str = Field(..., description="Mailbox to read emails from")
    verbose: bool = Field(False, description="Enable verbose output")
    imap_server: ImapServer = Field(
        ..., description="IMAP server (google, outlook, yahoo, custom)")
    custom_server: Optional[str] = Field(
        None, description="Custom IMAP server address (if --imap-server is 'custom')")
    filter: Optional[List[str]] = Field(
        None, description="Filter criteria for emails")
    rules: Optional[str] = Field(
        None, description="Parsing rules for email content")
    storage: StorageType = Field(...,
                                 description="Storage type (file, database)")
    output_format: OutputFormat = Field(
        ..., description="Output format for extracted data (json, csv)")
    log_file: Optional[str] = Field(
        None, description="Log file for verbose output")
    email_limit: int = Field(...,
                             description="Limit the number of emails to process")
    filter_accounts: Optional[str] = Field(
        None, description="List of email addresses to filter by")
    date_range: DateRange = Field(
        DateRange(days_ago=7), description="Date range for filtering emails")

    class Config:
        arbitrary_types_allowed = True
