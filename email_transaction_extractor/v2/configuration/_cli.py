import argparse
import os
import sys
from datetime import datetime
from pydantic import ValidationError
from ..models.options import CLIOptions
from ..models.enums import OutputFormat, StorageType, ImapServer
from ..models.dates import DateRange
from dotenv import load_dotenv


class CLIHandler:
    def __init__(self):
        load_dotenv()
        self.parser = argparse.ArgumentParser(
            description="Transaction Extractor: Extract transaction details from bank statements or emails."
        )
        self._add_arguments()
        self.args = self.parser.parse_args()

    def _add_arguments(self) -> CLIOptions:
        self.parser.add_argument(
            '-u', '--user',
            required=True,
            help='Email account username'
        )
        self.parser.add_argument(
            '-p', '--password',
            help='Email account password',
            default=os.getenv('EMAIL_PASSWORD')
        )
        self.parser.add_argument(
            '-m', '--mailbox',
            required=True,
            help='Mailbox to read emails from'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        self.parser.add_argument(
            '-i', '--imap-server',
            required=True,
            type=str,
            choices=[e.value for e in ImapServer],
            help='IMAP server (google, outlook, yahoo, custom)'
        )
        self.parser.add_argument(
            '--custom-server',
            help='Custom IMAP server address (if --imap-server is "custom")'
        )
        self.parser.add_argument(
            '-f', '--filter',
            nargs='+',
            help='Filter criteria for emails (e.g., sender:bank@example.com, subject:Transaction Alert). Multiple values should be separated by space.'
        )
        self.parser.add_argument(
            '-r', '--rules',
            help='Parsing rules for email content'
        )
        self.parser.add_argument(
            '-s', '--storage',
            required=True,
            type=str,
            choices=[e.value for e in StorageType],
            help='Storage type (file, database)'
        )
        self.parser.add_argument(
            '-o', '--output-format',
            required=True,
            type=str,
            choices=[e.value for e in OutputFormat],
            help='Output format for extracted data (json, csv)'
        )
        self.parser.add_argument(
            '-l', '--log-file',
            help='Log file for verbose output'
        )
        self.parser.add_argument(
            '-n', '--email-limit',
            type=int,
            required=True,
            help='Limit the number of emails to process'
        )
        self.parser.add_argument(
            '--filter-accounts',
            help='List of email addresses to filter by'
        )

        date_group = self.parser.add_mutually_exclusive_group()
        date_group.add_argument(
            '--days-ago',
            type=int,
            help='Date range for filtering emails in the past days (e.g., 7 for past 7 days)'
        )
        date_group.add_argument(
            '--start-date',
            type=lambda d: datetime.strptime(d, '%Y-%m-%d'),
            help='Start date for the date range (format: YYYY-MM-DD)'
        )
        date_group.add_argument(
            '--end-date',
            type=lambda d: datetime.strptime(d, '%Y-%m-%d'),
            help='End date for the date range (format: YYYY-MM-DD)'
        )

    def parse_args(self) -> CLIOptions:
        args = vars(self.args)
        try:
            # Handling the conversion of date_range separately
            days_ago = args.pop('days_ago', None)
            start_date = args.pop('start_date', None)
            end_date = args.pop('end_date', None)

            if days_ago is not None:
                date_range = DateRange(days_ago=days_ago)
            elif start_date is not None and end_date is not None:
                date_range = DateRange(
                    start_date=start_date, end_date=end_date)
            else:
                date_range = DateRange(days_ago=7)

            cli_args = CLIOptions(**args, date_range=date_range)
        except ValidationError as e:
            print(e.json())
            sys.exit(1)
        return cli_args

    def print_config(self):
        args_dict = vars(self.args)
        print("Configuration:")
        for key, value in args_dict.items():
            print(f"{key}: {value}")
