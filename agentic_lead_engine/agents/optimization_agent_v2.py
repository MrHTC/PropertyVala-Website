from typing import Dict

from agentic_lead_engine.utils.logger import Logger


class OptimizationAgentV2:
    def __init__(self):
        self.logger = Logger("Optimization")

    def suggest_improvements(self, metrics: Dict[str, int]) -> Dict[str, str]:
        suggestions = {}
        if metrics.get("contact_rate", 0) < 70:
            suggestions["outreach"] = "Increase HOT lead filtering and improve message personalization."
        if metrics.get("reply_rate", 0) < 15:
            suggestions["message"] = "Test a second outreach variant with a stronger offer and clearer next step."
        if metrics.get("conversion_rate", 0) < 20:
            suggestions["followup"] = "Add one more follow-up after 48 hours for interested respondents."
        if not suggestions:
            suggestions["status"] = "Performance looks stable; keep scaling progressively."
        self.logger.info("Generated optimization suggestions")
        return suggestions
