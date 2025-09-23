class Tax:
    def __init__(self, tax: float = 0.0, name: str = '', scope: list | None = None, assetClassScope: list | None = None):
        self.tax = float(tax)
        self.name = name
        self.scope = scope or []
        self.assetClassScope = assetClassScope or []