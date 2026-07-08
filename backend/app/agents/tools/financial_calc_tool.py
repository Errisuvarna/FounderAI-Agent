"""
Real tool calling: deterministic financial calculator.
Ensures the Finance agent produces mathematically consistent numbers
(CAC, LTV, break-even, 3-year revenue projection) instead of letting the LLM
guess at arithmetic, which is a common source of hallucinated figures.
"""
import json

from crewai_tools import BaseTool


class FinancialCalculatorTool(BaseTool):
    name: str = "financial_calculator"
    description: str = (
        "Perform startup financial calculations. Input must be a JSON string with keys: "
        "avg_price_per_unit (float), monthly_customers_year1 (int), "
        "monthly_growth_rate (float, e.g. 0.08 for 8%), "
        "customer_acquisition_cost (float), gross_margin (float, e.g. 0.7 for 70%), "
        "fixed_monthly_costs (float), avg_customer_lifetime_months (int). "
        "Returns computed LTV, LTV:CAC ratio, 3-year revenue projection, and break-even month."
    )

    def _run(self, input_json: str) -> str:
        try:
            params = json.loads(input_json)
            price = float(params["avg_price_per_unit"])
            start_customers = int(params["monthly_customers_year1"])
            growth_rate = float(params["monthly_growth_rate"])
            cac = float(params["customer_acquisition_cost"])
            gross_margin = float(params["gross_margin"])
            fixed_costs = float(params["fixed_monthly_costs"])
            lifetime_months = int(params["avg_customer_lifetime_months"])
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            return (
                f"Invalid input for financial_calculator: {exc}. "
                "Provide a valid JSON object with all required numeric keys."
            )

        # LTV & unit economics
        ltv = price * gross_margin * lifetime_months
        ltv_to_cac = round(ltv / cac, 2) if cac > 0 else None

        # 36-month revenue projection with compounding monthly growth
        monthly_revenue = []
        customers = start_customers
        cumulative_profit = -fixed_costs  # month 0 baseline
        break_even_month = None
        for month in range(1, 37):
            revenue = customers * price
            gross_profit = revenue * gross_margin
            monthly_revenue.append(round(revenue, 2))
            cumulative_profit += gross_profit - fixed_costs
            if break_even_month is None and cumulative_profit >= 0:
                break_even_month = month
            customers = int(customers * (1 + growth_rate))

        year1_total = round(sum(monthly_revenue[0:12]), 2)
        year2_total = round(sum(monthly_revenue[12:24]), 2)
        year3_total = round(sum(monthly_revenue[24:36]), 2)

        result = {
            "ltv": round(ltv, 2),
            "cac": cac,
            "ltv_to_cac_ratio": ltv_to_cac,
            "year1_revenue": year1_total,
            "year2_revenue": year2_total,
            "year3_revenue": year3_total,
            "break_even_month": break_even_month or "beyond 36 months at current assumptions",
            "healthy_unit_economics": bool(ltv_to_cac and ltv_to_cac >= 3),
        }
        return json.dumps(result, indent=2)
