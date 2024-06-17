from .models.email import Mail
from .services.transaction_report_service import TransactionReport
from .configuration import CLIHandler
from .email import IMAPSearchCriteria
from .services import EmailService
from .authentication import EmailClient


def main():
    cli = CLIHandler()
    cli_args = cli.parse_args()
    cli.print_config()
    report = TransactionReport(cli_args)
    report()
