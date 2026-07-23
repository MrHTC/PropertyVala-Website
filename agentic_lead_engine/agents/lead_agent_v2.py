from typing import Dict, List

from agentic_lead_engine.agents.lead_source_adapter import LeadSourceAdapter
from agentic_lead_engine.utils.logger import Logger


class LeadAgentV2:
    def __init__(self):
        self.logger = Logger("LeadAgent")
        self.adapter = LeadSourceAdapter()

    def fetch_leads(self, niche: str, location: str, limit: int = 50) -> List[Dict]:
        self.logger.info(f"Fetching leads for {niche} in {location} using {self.adapter.source_type} source")
        return self.adapter.fetch_leads(niche, location, limit)

    def validate_leads(self, leads: List[Dict]) -> List[Dict]:
        validated = [
            lead for lead in leads
            if lead.get("phone") and lead.get("phone").strip() and lead.get("gmb_status") != "Not Listed"
        ]
        self.logger.info(f"Validated {len(validated)} / {len(leads)} leads")
        return validated
