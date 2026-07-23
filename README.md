# Agentic Lead Engine

A modular Python framework for lead sourcing, qualification, outreach, and commission tracking. Built for solopreneurs and agencies who need verified buyer intent leads with enforced payouts.

## What It Does

1. **Fetches leads** from CSV files, APIs, or built-in mock data. Supports real estate portal stubs (Magicbricks, 99acres, Housing.com).
2. **Scores leads** 0-100 using a 6-factor model (contact info, legitimacy, financials, engagement, location/demand, digital presence).
3. **Classifies** leads into HOT / WARM / COLD tiers.
4. **Sends outreach** via WhatsApp or saved message templates.
5. **Tracks commissions** with platform/source splits, late fees, and 60-day service suspension rules.
6. **Auto-selects the best source** when configured with multiple sources.

Default niche is real estate and default city is Delhi. You can change this in `.env`.

## Quick Start

```bash
git clone https://github.com/MrHTC/AGENTIC-LEAD-ENGINE.git
cd AGENTIC-LEAD-ENGINE
cp .env.example .env
pip install -r requirements.txt
python run.py cycle real_estate Delhi
```

## CLI Commands

```bash
python run.py cycle <niche> <city>
python run.py leads <niche> <city>
python run.py validate <niche> <city>
python run.py api
```

### Examples

```bash
python run.py cycle residential_land Delhi
python run.py leads real_estate Gurgaon
python run.py validate apartment Noida
python run.py api
```

## Configuration

Copy `.env.example` to `.env` and adjust:

| Variable | Default | Description |
|----------|---------|-------------|
| `V2_LEAD_SOURCE` | `real_estate` | Source mode: `mock`, `csv`, `api`, `csv+api`, `auto`, `real_estate` |
| `V2_LEAD_SOURCE_ORDER` | `real_estate,csv,api,mock` | Source fallback order |
| `V2_DEFAULT_CITY` | `delhi` | Default city |
| `V2_DEFAULT_PROPERTY_TYPE` | `residential_land` | Default property type |
| `V2_LEAD_SOURCE_CSV_PATH` | — | Path to leads CSV |
| `V2_LEAD_SOURCE_API_URL` | — | API source URL |
| `V2_LEAD_SOURCE_API_KEY` | — | API source key |
| `MOBILE_CRM_API_KEY` | `changeme` | API key for mobile CRM endpoints |
| `COMMISSION_CONVERSION_PLATFORM` | `10.0` | % platform cut on deal closure |
| `COMMISSION_CONVERSION_SOURCE` | `3.0` | % source partner cut on deal closure |
| `LATE_PAYMENT_GRACE_DAYS` | `15` | Grace period before late fees |
| `LATE_PAYMENT_PENALTY_PERCENT_PER_WEEK` | `2.0` | Weekly late fee % |
| `PAYMENT_SUSPENSION_AFTER_DAYS` | `60` | Days after which access is suspended |
| `OLLAMA_API_URL` | `http://127.0.0.1:11434/v1/outputs` | Ollama server (optional) |
| `WHATSAPP_API_URL` | — | WhatsApp API URL (optional) |

## Mobile CRM API

Run the API server:

```bash
python run.py api
```

Endpoints (all require `X-API-KEY` or `?api_key=` if `MOBILE_CRM_API_KEY` is set):

- `GET /api/health`
- `GET /api/leads`
- `GET /api/leads/<id>`
- `PATCH /api/leads/<id>/status`
- `POST /api/leads/<id>/notes`
- `POST /api/leads/<id>/followups`
- `GET /api/leads/<id>/analytics`
- `GET /api/dashboard`

## Project Structure

```
AGENTIC-LEAD-ENGINE/
├── agents/
│   ├── lead_source_adapter.py       # CSV / API / mock / real-estate portal sources
│   ├── qualification_agent_v2.py    # 6-factor scoring + tiers
│   ├── outreach_agent_v2.py         # WhatsApp templates
│   ├── commission_agent.py          # Splits, late fees, suspension
│   ├── analytics_agent_v2.py        # Metrics
│   ├── conversion_agent_v2.py       # Pricing + referral routing
│   ├── followup_agent_v2.py         # Follow-up scheduling
│   ├── sales_agent_v2.py            # Reply handling
│   ├── lead_agent_v2.py             # Validation
│   └── optimization_agent_v2.py     # Suggestions
├── orchestrator/
│   └── orchestrator.py              # Main pipeline
├── api/
│   ├── mobile_crm.py                # CRM logic
│   └── mobile_crm_server.py         # Flask server
├── utils/
│   ├── csv_memory.py                # Memory tables: leads, contacted, replies, conversions, commissions, invoices
│   ├── logger.py                    # Logging
│   ├── ollama_client.py             # AI classification
│   └── whatsapp_sender.py           # WhatsApp integration
├── config/
│   └── settings.py                  # Environment settings
├── docs/
│   ├── contracts/                   # Service agreement, lead buyer agreement
│   ├── legal/                       # Terms of service, privacy policy
│   └── policies/                    # Commission, late payment, quality SLA
├── requirements.txt
├── .env.example
├── .gitignore
└── run.py                           # CLI entry point
```

## Lead Scoring Model

Every lead gets a 0-100 score across:

- **Contact info** (0-20): phone, email, location
- **Business legitimacy** (0-20): GMB status, category, team size
- **Financial indicators** (0-15): price range, budget signals
- **Engagement readiness** (0-15): existing score, tags, timeline
- **Market demand** (0-15): location presence, niche match
- **Digital presence** (0-15): email, website

Tiers:

| Tier | Score range |
|------|-------------|
| COLD | 0-59 |
| WARM | 60-84 |
| HOT | 85-100 |

## Commission & Payment Rules

- On deal closure: platform gets 10%, source partner gets 3%
- Invoice due Net 15
- Late fee: 2% per week after 15-day grace
- Suspension: after 60 days overdue
- TDS: 1% under Section 194H (India)

## Without Ollama

If Ollama is not running, the system falls back to rule-based scoring and classification. Everything else works without external AI.

## Requirements

- Python 3.9+
- Flask (for API mode)
- See `requirements.txt`

## License

MIT
