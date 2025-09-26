from typing import Dict, Any, List
from models.tax import Tax
from models.operation import Operation, OperationType

class Compute:
    def __init__(self, input_data: Dict[str, Any]):
        self.input = input_data or {}
        self.result: Dict[str, Any] = {}

        # Carrega operações
        ops_in = self.input.get("operations", [])
        self.operations_list: List[Operation] = [
            Operation(**op) for op in ops_in if isinstance(op, dict)
        ]

        # Carrega taxes (lista ou dict único)
        raw_taxes = self.input.get("taxes", [])
        if isinstance(raw_taxes, dict):
            self.taxes: List[Tax] = [Tax(**raw_taxes)]
        elif isinstance(raw_taxes, list):
            self.taxes = [Tax(**t) for t in raw_taxes if isinstance(t, dict)]
        else:
            self.taxes = []

    def _applies_to_class(self, tx: Tax, asset_class: str) -> bool:
        """
        Se a Tax tiver assetClassScope, respeita; senão, aplica para todos.
        """
        scope_list = getattr(tx, "assetClassScope", None)
        if not scope_list:
            return True
        return asset_class in scope_list

    def calculate(self) -> Dict[str, Any]:
        if not self.operations_list:
            return {"grossProfit": 0.0, "taxes": 0.0, "netProfit": 0.0, "finalValue": 0.0}

        # (Opcional) ordenar se existir date no seu modelo
        # self.operations_list.sort(key=lambda o: getattr(o, "date", ""))

        # Vamos consolidar por assetClass (compatível com os seus testes "pleno")
        classes = list({getattr(op, "assetClass", "default") for op in self.operations_list})
        by_class: Dict[str, Dict[str, Any]] = {}

        total_buy_notional_all = 0.0
        total_realized_gross_all = 0.0
        total_taxes_all = 0.0
        total_net_all = 0.0

        for cls in classes:
            # Estado por classe
            total_qty = 0.0
            total_cost = 0.0
            avg_cost = 0.0

            realized_gross = 0.0
            buy_notional = 0.0
            turnover = 0.0  # soma dos notionais de TODAS as ops (buy+sell) dessa classe

            # 1) Caminho de composição de posição + PnL
            for op in self.operations_list:
                if getattr(op, "assetClass", "default") != cls:
                    continue

                notional = op.unitCost * op.quantity
                turnover += notional

                if op.operation == OperationType.BUY:
                    # atualiza posição
                    total_qty += op.quantity
                    total_cost += notional
                    avg_cost = total_cost / total_qty if total_qty else 0.0

                    # buy notional (pra finalValue)
                    buy_notional += notional

                elif op.operation == OperationType.SELL:
                    # realiza PnL com avg_cost vigente
                    realized_gross += (op.unitCost - avg_cost) * op.quantity

                    # atualiza posição
                    total_qty -= op.quantity
                    total_cost -= avg_cost * op.quantity
                    avg_cost = (total_cost / total_qty) if total_qty else 0.0

            # 2) Taxes por classe
            taxes_for_class = 0.0
            for tx in self.taxes:
                if not self._applies_to_class(tx, cls):
                    continue

                scope = getattr(tx, "scope", None)
                rate = float(getattr(tx, "tax", 0.0) or 0.0)

                # IR/IOF: incidem sobre lucro realizado POSITIVO
                if scope == "sell" and realized_gross > 0:
                    # name pode ser "IR", "IOF" etc. — aqui tratamos ambos igual
                    taxes_for_class += realized_gross * rate

                # custody: ad valorem sobre o turnover (both = compra+venda)
                if scope == "both":
                    taxes_for_class += turnover * rate

                # fixedFee (se existir) — soma direto (1x por classe aqui)
                fixed = getattr(tx, "fixedFee", None)
                if isinstance(fixed, (int, float)) and fixed > 0:
                    taxes_for_class += float(fixed)

            realized_net = realized_gross - taxes_for_class
            final_value_at_cost = buy_notional + realized_net  # sem MTM

            by_class[cls] = {
                "realizedGrossPnL": round(realized_gross, 6),
                "totalTaxes": round(taxes_for_class, 6),
                "realizedNetPnL": round(realized_net, 6),
                "remainingPosition": {
                    "quantity": total_qty,
                    "avgCost": round(avg_cost, 6),
                },
                "finalValueAtCost": round(final_value_at_cost, 6),
            }

            # soma nos totais
            total_buy_notional_all += buy_notional
            total_realized_gross_all += realized_gross
            total_taxes_all += taxes_for_class
            total_net_all += realized_net

        # Saída total (agregada)
        self.result = {
            "byAssetClass": by_class,
            "total": {
                "realizedGrossPnL": round(total_realized_gross_all, 6),
                "totalTaxes": round(total_taxes_all, 6),
                "realizedNetPnL": round(total_net_all, 6),
                "finalValueAtCost": round(total_buy_notional_all + total_net_all, 6),
            },
        }
        return self.result
