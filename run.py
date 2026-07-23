"""
Agentic Lead Engine — CLI entry point

Usage:
    python run.py cycle <niche> <city>
    python run.py leads <niche> <city>
    python run.py validate <niche> <city>
    python run.py api
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agentic_lead_engine.config import settings
from agentic_lead_engine.orchestrator.orchestrator import Orchestrator
from agentic_lead_engine.agents.lead_source_adapter import LeadSourceAdapter
from agentic_lead_engine.utils.logger import Logger


def main():
    logger = Logger("CLI")
    mode = sys.argv[1] if len(sys.argv) > 1 else "help"
    niche = sys.argv[2] if len(sys.argv) > 2 else settings.DEFAULT_PROPERTY_TYPE
    location = sys.argv[3] if len(sys.argv) > 3 else settings.DEFAULT_CITY

    if mode == "cycle":
        logger.info(f"Running single cycle for {niche} in {location}")
        orchestrator = Orchestrator()
        summary = orchestrator.run_cycle(niche, location)
        print(summary)

    elif mode == "leads":
        adapter = LeadSourceAdapter()
        leads = adapter.fetch_leads(niche, location, limit=50)
        print(f"Fetched {len(leads)} leads for {niche} in {location}")
        for lead in leads[:5]:
            print(f"  - {lead.get('name')} | {lead.get('phone')} | score={lead.get('score', 'N/A')}")

    elif mode == "validate":
        logger.info(f"Validating market demand for {niche} in {location}")
        print(f"Niche: {niche}, Location: {location}")
        print("Market validation module can be plugged into Orchestrator.run_cycle()")

    elif mode == "api":
        logger.info("Starting Mobile CRM API server")
        from agentic_lead_engine.api.mobile_crm_server import app
        port = int(os.getenv("PORT", "5000"))
        app.run(host="0.0.0.0", port=port)

    else:
        print("""
Agentic Lead Engine — CLI

Usage: python run.py [mode] [niche] [city]

Modes:
  cycle       Run full lead -> qualify -> outreach -> analytics cycle
  leads       Fetch leads from configured source
  validate    Validate market demand for niche/city
  api         Start Mobile CRM API server (port 5000)

Examples:
  python run.py cycle real_estate Delhi
  python run.py leads residential_land Gurgaon
  python run.py validate apartment Noida
  python run.py api

Environment:
  Copy .env.example to .env and fill values.
  See README.md for full configuration options.
        """)


if __name__ == "__main__":
    main()
