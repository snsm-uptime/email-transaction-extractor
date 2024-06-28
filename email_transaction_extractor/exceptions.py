class TransactionIDExistsError(Exception):
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        super().__init__(f"Transaction with ID {
            transaction_id} already exists.")
