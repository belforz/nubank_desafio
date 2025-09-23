def validate_action(input_data: dict) -> None:
    ops = input_data.get("operations", [])
    taxes = input_data.get("taxes", 0)
    if not isinstance(ops, list) or len(ops) != 2:
        raise ValueError("Invalid operations format")
    buy, sell = ops
    if buy.get("operation") != "buy" or sell.get("operation") != "sell":
        raise ValueError("Operations must be 'buy' followed by 'sell'")
    
    sell, both = taxes
    if sell.get("scope") != 'sell' or both.get("scope") != 'both':
        raise ValueError("Tax scope must be 'sell' or 'both'")
    
    
    # raw_tax = input_data.get("tax", {})
    # tax_value = None

    
    # if isinstance(raw_tax, (int, float)):
    #     tax_value = raw_tax
    # elif isinstance(raw_tax, dict):
    #     for t in ("tax_value", "tax", "tax_number"):
    #         val = raw_tax.get(t)
    #         if isinstance(val, (int, float)):
    #             tax_value = val
    #             break

    # if tax_value is None or tax_value < 0:
    #     raise ValueError("Tax must be a non-negative number")

    return None