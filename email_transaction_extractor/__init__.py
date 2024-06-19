import logging
import os

from .models.enums import StorageType
from .utils.logging import configure_root_logger
from .services.transaction_report import TransactionReport
from .configuration import CLIHandler


def main():
    cli = CLIHandler()
    cli_args = cli.parse_args()
    configure_root_logger('transaction_extractor', log_level=logging.DEBUG if cli_args.verbose else logging.INFO,
                          log_file=os.getenv('LOG_FILE', 'app.log'))
    cli.log_config()
    report = TransactionReport(cli_args)
    if cli_args.storage is not StorageType.FILE:
        df = report.get_dataframe()
    else:
        report.persist_data()
