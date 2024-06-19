from ..models.item import Item
from ._base_repository import BaseRepository


class PostgresRepository(BaseRepository):
    def __init__(self, db_config: dict):
        db_url = f"postgresql://{db_config['user']}:{
            db_config['password']}@{db_config['host']}/{db_config['dbname']}"
        super().__init__(db_url)
        self.create_tables()

    def add(self, item: Item) -> None:
        with self.session_scope() as session:
            session.add(item)

    def get(self, item_id: int) -> Item:
        with self.session_scope() as session:
            return session.query(Item).filter(Item.id == item_id).one_or_none()

    def update(self, item: Item) -> None:
        with self.session_scope() as session:
            existing_item = session.query(Item).filter(
                Item.id == item.id).one_or_none()
            if existing_item:
                existing_item.name = item.name
                existing_item.description = item.description

    def delete(self, item_id: int) -> None:
        with self.session_scope() as session:
            item = session.query(Item).filter(Item.id == item_id).one_or_none()
            if item:
                session.delete(item)
