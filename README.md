
# Project Details
## Requirements
```sh
# Install dependencies
poetry install
```
### Environment Variables
```sh
EMAIL_USER="<your-email>"
EMAIL_PASSWORD="***"
LOG_FILE="server.log"
DATABASE_URL="postgresql://<username>:<password>@<host>:5432/<database>"
```

## Folder Structure

```sh
my_email_transaction_app/
├── alembic/
│   ├── versions/
│   └── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── transaction.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── transaction_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── transactions.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── transaction.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transaction_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── email_reader.py
│   ├── tests/
│       ├── __init__.py
│       ├── test_transactions.py
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

### Detailed Explanation
- alembic/: Directory for Alembic migrations.
    - versions/: Directory for storing migration scripts.
    - env.py: Alembic environment configuration file.
    - script.py.mako: Template for new migration scripts.
- app/: Main application directory.
    - init.py: Marks the directory as a Python package.
    - config.py: Configuration settings for the application.
    - database.py: Database setup and session management.
    - main.py: Entry point for the FastAPI application.
    - models/: Directory for SQLAlchemy models.
        - init.py: Marks the directory as a Python package.
        - enums.py: Enum classes for the application.
        - transaction.py: Transaction model definition.
    - repositories/: Directory for repository classes that handle database operations.
        - init.py: Marks the directory as a Python package.
        - transaction_repository.py: Repository for transaction-related database operations.
    - routers/: Directory for FastAPI route handlers.
        - init.py: Marks the directory as a Python package.
        - transactions.py: Route handlers for transaction-related endpoints.
    - schemas/: Directory for Pydantic models (schemas) used for data validation.
        - init.py: Marks the directory as a Python package.
        - transaction.py: Pydantic models for transactions.
    - services/: Directory for business logic services.
        - init.py: Marks the directory as a Python package.
        - transaction_service.py: Service layer for transaction-related operations.
    - utils/: Directory for utility functions and classes.
        - init.py: Marks the directory as a Python package.
        - email_reader.py: Utility for reading and filtering emails.
- tests/: Directory for unit and integration tests.
    - init.py: Marks the directory as a Python package.
    - test_transactions.py: Test cases for transaction functionality.
- .env: Environment variables file (e.g., database URL, email credentials).
- .gitignore: Git ignore file to exclude unnecessary files from version control.
- pyproject.toml: Poetry configuration file.
- README.md: Project documentation.