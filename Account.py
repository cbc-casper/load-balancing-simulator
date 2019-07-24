class Account:
    def __init__(self, id, gas_size=0, storage_size=0, linked_accounts=[], linked_accounts_tx_count={}):
        self.id = id
        self.gas_size = gas_size
        self.storage_size = storage_size
        self.linked_accounts = linked_accounts
        self.linked_accounts_tx_count = linked_accounts_tx_count
