from typing import Dict, List

from agentic_lead_engine.utils.logger import Logger
from agentic_lead_engine.utils.whatsapp_sender import WhatsAppSender


class OutreachAgentV2:
    def __init__(self, whatsapp_sender: WhatsAppSender):
        self.whatsapp_sender = whatsapp_sender
        self.logger = Logger("Outreach")
        self.templates = {
            "gym": [
                "Hi {name}, quick question: are you actively using GMB for {location}? We help gyms get more walk-ins with simple WhatsApp follow-ups.",
                "Hey {name}, 2 quick lines: boost your gym's GMB reviews and convert local search into paying members. Interested?"
            ],
            "hvac": [
                "Hi {name}, do you want more HVAC repair leads from Google My Business? We can automate WhatsApp follow-up in 48h.",
                "Hey {name}, quick idea: turn your GMB traffic into booked HVAC jobs with a 2-step WhatsApp funnel. Want details?"
            ],
            "salon": [
                "Hi {name}, can your salon get more bookings from GMB without extra ads? We send a simple WhatsApp message that converts.",
                "Hey {name}, 2-line plan: boost your salon photo reviews and turn local search into appointments. Shall I share it?"
            ],
            "real_estate": [
                "Hi {name}, are you getting enough qualified property enquiries in Meerut? We help real estate teams convert GMB traffic into booked site visits via WhatsApp.",
                "Hey {name}, quick idea: turn your Meerut property listings into hot leads with a simple WhatsApp follow-up and appointment booking flow. Want to see a sample?"
            ],
            "default": [
                "Hi {name}, quick question: are you reaching your ideal customers in {location}? We help local businesses convert online demand into more appointments.",
                "Hey {name}, small changes to your WhatsApp outreach can turn more local searches into paying clients. Want a fast audit?"
            ]
        }

    def send_outreach(self, leads: List[Dict], niche: str, location: str, limit: int = 40) -> List[Dict]:
        sent = []
        seen = set()
        template_set = self.templates.get(niche, self.templates["gym"])

        for index, lead in enumerate(leads[:limit]):
            phone = str(lead.get("phone", ""))
            if not phone or phone in seen:
                continue
            seen.add(phone)

            name = lead.get("name", "there").split()[0]
            message = template_set[index % len(template_set)].format(
                name=name,
                location=lead.get("location", "your area")
            )

            success = self.whatsapp_sender.send_with_retry(phone, message)
            status = "sent" if success else "skipped"
            record = {
                "lead_id": lead.get("id"),
                "phone": phone,
                "message": message,
                "channel": "whatsapp",
                "status": status
            }
            sent.append(record)
            self.logger.info(f"Outreach {status} for {phone}")

        self.logger.info(f"Prepared {len(sent)} outreach records")
        return sent
