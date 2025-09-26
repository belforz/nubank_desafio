def validate_action(input_data: dict) -> None:
    
    if not isinstance(input_data, dict):
        raise ValueError("input must be a JSON object")

    ops = input_data.get("operations")
    if not isinstance(ops, list) or len(ops) == 0:
        raise ValueError("operations must be a non-empty list")

    
    if ops[0].get("operation") != "buy":
        raise ValueError("first operation must be 'buy'")
    if not any(o.get("operation") == "sell" for o in ops):
        raise ValueError("there must be at least one 'sell' operation")

   
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            raise ValueError(f"operation {i} must be an object")
        if not isinstance(op.get("unitCost"), (int, float)) or op.get("unitCost") < 0:
            raise ValueError(f"operation {i} has invalid unitCost")
        if not isinstance(op.get("quantity"), int) or op.get("quantity") <= 0:
            raise ValueError(f"operation {i} has invalid quantity")

    taxes = input_data.get("taxes")
    if not isinstance(taxes, list) or len(taxes) == 0:
        raise ValueError("taxes must be a non-empty list")

    for j, tx in enumerate(taxes):
        if not isinstance(tx, dict):
            raise ValueError(f"tax {j} must be an object")
        if not isinstance(tx.get("tax"), (int, float)) or tx.get("tax") < 0:
            raise ValueError(f"tax {j} has invalid tax value")

    return None