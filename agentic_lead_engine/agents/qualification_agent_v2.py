from typing import Dict, List

from agentic_lead_engine.utils.logger import Logger
from agentic_lead_engine.utils.ollama_client import OllamaClient


class QualificationAgentV2:
    def __init__(self, ollama: OllamaClient):
        self.ollama = ollama
        self.logger = Logger("Qualification")

    def classify_leads(self, leads: List[Dict]) -> List[Dict]:
        results = []
        for lead in leads:
            lead = self._enrich_with_score(lead)
            quality = self._tier_from_score(lead.get("score", 0))
            lead["quality"] = quality
            results.append(lead)
        self.logger.info(f"Classified {len(results)} leads")
        return results

    def _enrich_with_score(self, lead: Dict) -> Dict:
        score = self._compute_score(lead)
        lead["score"] = score
        lead["score_breakdown"] = {
            "contact_info": self._score_contact_info(lead),
            "business_legitimacy": self._score_business_legitimacy(lead),
            "financial_indicators": self._score_financial_indicators(lead),
            "engagement_readiness": self._score_engagement_readiness(lead),
            "market_demand": self._score_market_demand(lead),
            "digital_presence": self._score_digital_presence(lead),
        }
        return lead

    def _compute_score(self, lead: Dict) -> int:
        return int(sum([
            self._score_contact_info(lead),
            self._score_business_legitimacy(lead),
            self._score_financial_indicators(lead),
            self._score_engagement_readiness(lead),
            self._score_market_demand(lead),
            self._score_digital_presence(lead),
        ]))

    def _score_contact_info(self, lead: Dict) -> int:
        score = 0
        phone = str(lead.get("phone", "")).strip()
        email = str(lead.get("email", "")).strip()
        if phone and len(phone) >= 10:
            score += 10
        if email and "@" in email:
            score += 5
        if lead.get("location"):
            score += 5
        return min(score, 20)

    def _score_business_legitimacy(self, lead: Dict) -> int:
        score = 0
        if str(lead.get("gmb_status", "")).lower() == "active":
            score += 10
        if lead.get("category") or lead.get("niche"):
            score += 5
        if lead.get("estimated_members") and int(lead.get("estimated_members", 0)) > 0:
            score += 5
        return min(score, 20)

    def _score_financial_indicators(self, lead: Dict) -> int:
        score = 0
        price_range = str(lead.get("price_range", "")).strip()
        if price_range:
            score += 8
        if any(char.isdigit() for char in price_range):
            score += 7
        return min(score, 15)

    def _score_engagement_readiness(self, lead: Dict) -> int:
        score = 0
        if lead.get("score") and int(lead.get("score", 0)) >= 60:
            score += 5
        if lead.get("date_added"):
            score += 5
        tags = lead.get("tags") or []
        if any(tag in ["interested", "follow_up", "hot"] for tag in tags):
            score += 5
        return min(score, 15)

    def _score_market_demand(self, lead: Dict) -> int:
        score = 0
        location = str(lead.get("location", "")).lower()
        if location:
            score += 10
        niche = str(lead.get("niche", "")).lower()
        if niche in ["real_estate", "property", "realty"]:
            score += 5
        return min(score, 15)

    def _score_digital_presence(self, lead: Dict) -> int:
        score = 0
        if lead.get("email"):
            score += 8
        if lead.get("website"):
            score += 7
        return min(score, 15)

    def _tier_from_score(self, score: int) -> str:
        if score >= 85:
            return "HOT"
        if score >= 60:
            return "WARM"
        return "COLD"
