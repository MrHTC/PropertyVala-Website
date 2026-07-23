from typing import Dict

from agentic_lead_engine.utils.csv_memory import CSVMemory
from agentic_lead_engine.utils.logger import Logger


class AnalyticsAgentV2:
    def __init__(self, memory: CSVMemory):
        self.memory = memory
        self.logger = Logger("Analytics")

    def compute_metrics(self) -> Dict[str, int]:
        leads = self.memory.get_leads()
        contacted = self.memory.get_contacted()
        replies = self.memory.get_replies()
        conversions = self.memory.get_conversions()

        metrics = {
            "leads_saved": len(leads),
            "contacted": len(contacted),
            "replies": len(replies),
            "conversions": len(conversions),
            "contact_rate": self._safe_ratio(len(contacted), len(leads)),
            "reply_rate": self._safe_ratio(len(replies), len(contacted)),
            "conversion_rate": self._safe_ratio(len(conversions), len(replies))
        }
        self.logger.info("Computed analytics metrics")
        return metrics

    def _safe_ratio(self, numerator: int, denominator: int) -> int:
        if denominator <= 0:
            return 0
        return int((numerator / denominator) * 100)
