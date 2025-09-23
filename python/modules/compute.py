from typing import Dict, Any

from models.tax import Tax
from models.operation import Operation, OperationType

class Compute:
    def __init__(self, input_data: Dict[str, Any]):
        self.input = input_data
        self.result: Dict[str, Any] = {}
        self.operations_list = [Operation(**op) for op in self.input.get("operations", []) if isinstance(op, dict)]

        raw_taxes = self.input.get("taxes", [])
        if isinstance(raw_taxes, dict):
            self.taxes = [Tax(**raw_taxes)]
        elif isinstance(raw_taxes, list):
            self.taxes = [Tax(**t) for t in raw_taxes if isinstance(t, dict)]
        else:
            self.taxes = []
        
    def calculate(self) -> Dict[str, Any]:
        gross_profit = 0.0
        final_value = 0.0
        
        
        for op in self.operations_list:
            gross_profit = gross_profit + (op.unitCost * op.quantity) if op.operation == OperationType.SELL else gross_profit - (op.unitCost * op.quantity)
            aux_buy = (op.unitCost * op.quantity) if op.operation == OperationType.BUY else 0.0
            aux_sell = op.unitCost if op.operation == OperationType.SELL else 0.0
            

        self.result["grossProfit"] = gross_profit
        
        taxes = 0.0 
        total_taxes = 0.0
        
        
        turnover = sum((op.unitCost * op.quantity) for op in self.operations_list)
        
        for tx in self.taxes:
            scope = tx.scope
            if scope == "sell" and gross_profit > 0:
                taxes = (gross_profit * tx.tax)
                total_taxes += taxes
                print("taxas dentro de sell:",taxes)
            elif scope == 'both' and turnover != 0:
                taxes = turnover * tx.tax
                total_taxes += taxes
                print("taxas dentro de both:",taxes)
        self.result["taxes"] = total_taxes
        
        net_profit = gross_profit - total_taxes
        final_value = aux_buy + ((aux_sell - self.operations_list[0].quantity) * self.operations_list[0].quantity) - total_taxes + gross_profit
        self.result["netProfit"] = net_profit
        self.result["finalValue"] = final_value
        
        return self.result
            
            
           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

# class Compute:
#     def __init__(self, input_data: Dict[str, Any]):
#         self.input = input_data or {}
#         self.result: Dict[str, Any] = {}
#         ops = self.input.get("operations", [])
#         self.operations_list = ops if isinstance(ops, list) else []

    
#         raw_tax = self.input.get("tax", {})
#         tax_number = None
#         if isinstance(raw_tax, (int, float)):
#             tax_number = raw_tax
#         elif isinstance(raw_tax, dict):
#             for key in ("tax_value", "tax", "tax_number"):
#                 val = raw_tax.get(key)
#                 if isinstance(val, (int, float)):
#                     tax_number = val
#                     break

       
#         self.tax_number = float(tax_number) if tax_number is not None else 0.0

#     def calculate(self) -> Dict[str, Any]:
        
#         gross_profit = 0.0
#         for op in self.operations_list:
#             if not isinstance(op, dict):
#                 continue
#             if op.get("operation") == "buy":
#                 gross_profit =  gross_profit - (op.get("unitCost", 0) * op.get("quantity", 0))
#             elif op.get("operation") == "sell":
#                 gross_profit = gross_profit + (op.get("unitCost", 0) * op.get("quantity", 0))

#         self.result["grossProfit"] = gross_profit

        
#         taxes = 0.0
#         if gross_profit > 0 and self.tax_number > 0:
#             taxes = gross_profit * self.tax_number

#         self.result["taxes"] = taxes
#         net_profit = gross_profit - taxes
#         self.result["netProfit"] = net_profit
#         return self.result