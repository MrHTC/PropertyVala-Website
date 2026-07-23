from typing import Dict

from agentic_lead_engine.utils.logger import Logger


class SalesAgentV2:
    def __init__(self):
        self.logger = Logger("Sales")

    def generate_reply(self, lead: Dict, previous_message: str) -> str:
        lead_name = lead.get("name", "partner").split()[0]
        reply = (
            f"Hi {lead_name}, thanks for your message. "
            "We can launch a simple campaign that turns your GMB views into booked calls in 7 days. "
            "What is your ideal monthly lead target?"
        )
        self.logger.info(f"Generated reply for {lead_name}")
        return reply

    def handle_objection(self, objection_text: str) -> str:
        objection_text = objection_text.lower()
        if "price" in objection_text:
            return (
                "I understand the concern about cost. Our model is built to recover the investment within the first month through new service bookings. "
                        "Can I show you the numbers for a similar business?"
            )
        if "time" in objection_text:
            return (
                "This is designed to save you time, not add more work. We handle the delivery and send you only the qualified leads. "
                        "Would you like a short demo?"
            )
        return (
            "Great question. We usually start with a fast audit and low-risk pilot so you can see the value before scaling. "
                    "Shall we book that?"
        )

    def push_cta(self, lead: Dict) -> str:
        return "If you'd like, I can book a 15-minute strategy call and share a simple growth plan for your business." 
