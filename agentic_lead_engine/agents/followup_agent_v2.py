from datetime import datetime, timedelta
from typing import Dict, List

from agentic_lead_engine.utils.logger import Logger


class FollowupAgentV2:
    def __init__(self):
        self.logger = Logger("Followup")

    def build_followups(self, contacted: List[Dict], threshold_hours: int = 24) -> List[Dict]:
        followups = []
        cutoff = datetime.now() - timedelta(hours=threshold_hours)
        for row in contacted:
            sent_at = row.get("sent_at")
            try:
                sent_time = datetime.fromisoformat(sent_at)
            except Exception:
                continue
            if sent_time <= cutoff and row.get("status") == "sent":
                message = self._followup_message(row)
                followups.append({
                    "lead_id": row.get("lead_id"),
                    "phone": row.get("phone"),
                    "message": message,
                    "channel": row.get("channel", "whatsapp")
                })
                self.logger.info(f"Built follow-up for {row.get('phone')}")
        return followups

    def _followup_message(self, row: Dict) -> str:
        return (
            "Hi there, I wanted to follow up on my earlier message. "
            "We help businesses turn GMB traffic into paying clients with one simple WhatsApp workflow. "
            "Is now a good time to chat?"
        )
