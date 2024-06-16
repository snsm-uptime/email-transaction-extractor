from .configuration import CLIHandler


def main():
    cli = CLIHandler()
    cli_args = cli.parse_args()
    cli.print_config()
