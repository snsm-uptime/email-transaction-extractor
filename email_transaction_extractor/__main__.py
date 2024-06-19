from .repositories import SQLiteRepository, PostgresRepository


def main():
    # Example SQLite usage
    sqlite_repo = SQLiteRepository('sqlite.db')
    item = Item(id=1, name='Test Item', description='This is a test item')
    sqlite_repo.add(item)
    print(sqlite_repo.get(1))

    # Example PostgreSQL usage
    db_config = {
        'dbname': 'testdb',
        'user': 'testuser',
        'password': 'testpass',
        'host': 'localhost'
    }
    postgres_repo = PostgresRepository(db_config)
    postgres_repo.add(item)
    print(postgres_repo.get(1))


if __name__ == '__main__':
    main()
