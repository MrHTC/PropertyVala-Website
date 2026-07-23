from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from agentic_lead_engine.utils.csv_memory import CSVMemory
from agentic_lead_engine.config import settings
from agentic_lead_engine.utils.logger import Logger


class CommissionAgent:
    """
    Handles commission calculation, tracking, invoicing, and late-payment enforcement.
    """

    def __init__(self, memory: CSVMemory = None):
        self.memory = memory or CSVMemory(settings.MEMORY_DIR)
        self.logger = Logger("CommissionAgent")

        self.commission_rates = {
            "conversion_platform": float(getattr(settings, "COMMISSION_CONVERSION_PLATFORM", "10.0")),
            "conversion_source": float(getattr(settings, "COMMISSION_CONVERSION_SOURCE", "3.0")),
            "lead_sale_platform": float(getattr(settings, "COMMISSION_LEAD_SALE_PLATFORM", "70.0")),
            "lead_sale_source": float(getattr(settings, "COMMISSION_LEAD_SALE_SOURCE", "30.0")),
        }

        self.late_payment = {
            "grace_days": int(getattr(settings, "LATE_PAYMENT_GRACE_DAYS", "15")),
            "penalty_percent_per_week": float(getattr(settings, "LATE_PAYMENT_PENALTY_PERCENT_PER_WEEK", "2.0")),
            "suspension_after_days": int(getattr(settings, "PAYMENT_SUSPENSION_AFTER_DAYS", "60")),
        }

    def calculate_commission(self, deal_value: float, lead_score: Optional[float] = None, commission_type: str = "conversion") -> Dict[str, any]:
        rate = self.commission_rates.get(f"{commission_type}_platform", 10.0)
        amount = round(deal_value * (rate / 100.0), 2)
        return {
            "deal_value": deal_value,
            "commission_type": commission_type,
            "rate": rate,
            "amount": amount,
            "currency": "INR",
            "calculated_at": datetime.now().isoformat(timespec="seconds")
        }

    def record_commission(self, lead_id: str, phone: str, deal_value: float, agent_id: str = "", source: str = "", commission_type: str = "conversion") -> Dict[str, any]:
        calc = self.calculate_commission(deal_value, commission_type=commission_type)
        row = {
            "lead_id": str(lead_id),
            "phone": str(phone),
            "agent_id": str(agent_id),
            "source": str(source),
            "deal_value": str(deal_value),
            "commission_type": str(commission_type),
            "rate": str(calc["rate"]),
            "amount": str(calc["amount"]),
            "currency": calc["currency"],
            "status": "pending",
            "penalty": "0",
            "due_date": (datetime.now() + timedelta(days=self.late_payment["grace_days"])).isoformat(timespec="seconds"),
            "created_at": calc["calculated_at"],
            "paid_at": ""
        }
        self.memory._append("commissions.csv", row)
        self.logger.info(f"Recorded {commission_type} commission {calc['amount']} INR for lead {lead_id}")
        return row

    def get_pending_commissions(self) -> List[Dict[str, str]]:
        return [row for row in self.memory._read("commissions.csv") if row.get("status") == "pending"]

    def mark_commission_paid(self, commission_id: str, paid_amount: float) -> Dict[str, any]:
        commissions = self.memory._read("commissions.csv")
        updated = None
        for row in commissions:
            if row.get("lead_id") == commission_id and row.get("status") == "pending":
                row["status"] = "paid"
                row["paid_at"] = datetime.now().isoformat(timespec="seconds")
                updated = row
                break
        if updated:
            self.memory.save_leads(commissions)
        self.logger.info(f"Commission {commission_id} marked paid: {paid_amount}")
        return updated or {}

    def apply_late_fees(self) -> List[Dict[str, str]]:
        commissions = self.memory._read("commissions.csv")
        updated_rows = []
        now = datetime.now()
        grace = self.late_payment["grace_days"]
        penalty = self.late_payment["penalty_percent_per_week"]
        for row in commissions:
            if row.get("status") != "pending":
                continue
            due = datetime.fromisoformat(row.get("due_date", now.isoformat()))
            if now > due:
                weeks_late = max(1, (now - due).days // 7)
                late_fee = round(float(row.get("amount", 0)) * (penalty / 100.0) * weeks_late, 2)
                row["penalty"] = str(late_fee)
                updated_rows.append(row)
        if updated_rows:
            self.memory.save_leads(commissions)
            self.logger.info(f"Applied late fees to {len(updated_rows)} commissions")
        return updated_rows

    def suspend_overdue_agents(self) -> List[str]:
        commissions = self.memory._read("commissions.csv")
        now = datetime.now()
        cutoff = self.late_payment["suspension_after_days"]
        suspended = set()
        for row in commissions:
            if row.get("status") != "pending":
                continue
            due = datetime.fromisoformat(row.get("due_date", now.isoformat()))
            if (now - due).days > cutoff:
                suspended.add(row.get("agent_id"))
        for agent in suspended:
            self.logger.warning(f"Agent {agent} suspended for overdue payments > {cutoff} days")
        return list(suspended)

    def get_commission_analytics(self) -> Dict[str, any]:
        commissions = self.memory._read("commissions.csv")
        total = sum(float(r.get("amount", 0)) for r in commissions)
        paid = sum(float(r.get("amount", 0)) for r in commissions if r.get("status") == "paid")
        pending = sum(float(r.get("amount", 0)) for r in commissions if r.get("status") == "pending")
        penalties = sum(float(r.get("penalty", 0)) for r in commissions)
        return {
            "total_commissions": round(total, 2),
            "paid": round(paid, 2),
            "pending": round(pending, 2),
            "penalties": round(penalties, 2),
            "count": len(commissions),
            "generated_at": datetime.now().isoformat(timespec="seconds")
        }