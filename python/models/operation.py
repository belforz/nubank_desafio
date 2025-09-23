class OperationType:
    BUY = "buy"
    SELL = "sell"

class Operation:
    def __init__(self, operation: OperationType, unitCost: int = 0, quantity: int = 0, assetClass: list | None = None):
        self.operation = operation
        self.unitCost = unitCost
        self.quantity = quantity
        self.assetClass = assetClass or []