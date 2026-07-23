import csv
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from agentic_lead_engine.config import settings
from agentic_lead_engine.utils.logger import Logger


class LeadSource:
    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        raise NotImplementedError


class MockLeadSource(LeadSource):
    def __init__(self):
        self.logger = Logger("MockLeadSource")
        self.names = {
            "gym": [
                "Fit Body",
                "Power Zone",
                "Elite Gym",
                "FitX",
                "Muscle Hub",
                "YogaFlow",
                "Core Strength",
                "Urban Fitness",
                "Peak Performance",
                "Iron Temple"
            ],
            "real_estate": [
                "Meerut Properties",
                "Prime Estates",
                "City Home Agents",
                "Urban Realty",
                "Property Hub",
                "Blue Roof Realtors",
                "Vista Homes",
                "Landmark Realty",
                "HomeFront",
                "Metro Estate"
            ],
            "default": [
                "Local Business",
                "Trusted Partner",
                "Premier Service",
                "Premium Realty",
                "Top Choice",
                "Leading Brand"
            ]
        }

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        names = self.names.get(niche, self.names["default"])
        leads = []
        for idx in range(limit):
            leads.append({
                "id": idx + 1,
                "name": f"{self.names.get(niche, self.names['default'])[idx % len(self.names.get(niche, self.names['default']))]} {location}",
                "category": niche,
                "niche": niche,
                "location": f"Sector {idx + 1}, {location}",
                "phone": f"98{900000000 + idx}",
                "email": f"lead{idx+1}@{niche}.com",
                "gmb_status": "Active",
                "price_range": "₹25,000/mo",
                "estimated_members": 0,
                "date_added": datetime.now().isoformat(timespec="seconds")
            })
        self.logger.info(f"Generated {len(leads)} mock leads")
        return leads


class CSVLeadSource(LeadSource):
    def __init__(self, csv_path: str):
        self.logger = Logger("CSVLeadSource")
        self.csv_path = Path(csv_path)

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        if not self.csv_path or not self.csv_path.exists() or not self.csv_path.is_file():
            self.logger.warn(f"CSV lead source missing or invalid: {self.csv_path}")
            return []

        leads = []
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, raw in enumerate(reader):
                if idx >= limit:
                    break
                leads.append(self._normalize(raw, idx + 1, niche, location))
        self.logger.info(f"Loaded {len(leads)} leads from CSV")
        return leads

    def _normalize(self, raw: Dict, idx: int, niche: str, location: str) -> Dict:
        return {
            "id": raw.get("id", idx),
            "name": raw.get("name", raw.get("business_name", f"Lead {idx}")),
            "category": raw.get("category", raw.get("niche", niche)),
            "niche": raw.get("niche", raw.get("category", niche)),
            "location": raw.get("location", raw.get("city", location)),
            "phone": raw.get("phone", raw.get("mobile", "")),
            "email": raw.get("email", ""),
            "gmb_status": raw.get("gmb_status", raw.get("listing_status", "Unknown")),
            "price_range": self._normalize_price(raw.get("price_range", raw.get("budget", ""))),
            "estimated_members": self._normalize_int(raw.get("estimated_members", raw.get("team_size", 0))),
            "date_added": raw.get("date_added", datetime.now().isoformat(timespec="seconds"))
        }

    def _normalize_int(self, value):
        if value is None:
            return 0
        if isinstance(value, int):
            return value
        text = str(value)
        digits = re.findall(r"\d+", text)
        return int(digits[0]) if digits else 0

    def _normalize_price(self, value):
        if value is None:
            return ""
        return str(value).strip()


class APILeadSource(LeadSource):
    def __init__(self, api_url: str, api_key: str):
        self.logger = Logger("APILeadSource")
        self.api_url = api_url
        self.api_key = api_key

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        if not self.api_url:
            self.logger.warn("API lead source URL not configured")
            return []

        try:
            import urllib.parse
            query = f"?niche={urllib.parse.quote(niche)}&location={urllib.parse.quote(location)}&limit={limit}"
            request = urllib.request.Request(
                self.api_url + query,
                headers={
                    "Content-Type": "application/json",
                    **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {})
                },
                method="GET"
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
                leads = [self._normalize(item, idx + 1, niche, location) for idx, item in enumerate(payload[:limit])]
                self.logger.info(f"Fetched {len(leads)} leads from API source")
                return leads
        except urllib.error.URLError as exc:
            self.logger.warn(f"Lead API request failed: {exc}")
        except Exception as exc:
            self.logger.warn(f"Lead API parse failed: {exc}")
        return []

    def _normalize(self, raw: Dict, idx: int, niche: str, location: str) -> Dict:
        return {
            "id": raw.get("id", idx),
            "name": raw.get("name", raw.get("business_name", f"Lead {idx}")),
            "category": raw.get("category", raw.get("niche", niche)),
            "niche": raw.get("niche", raw.get("category", niche)),
            "location": raw.get("location", raw.get("city", location)),
            "phone": raw.get("phone", raw.get("mobile", "")),
            "email": raw.get("email", ""),
            "gmb_status": raw.get("gmb_status", raw.get("listing_status", "Unknown")),
            "price_range": raw.get("price_range", raw.get("budget", "")),
            "estimated_members": int(raw.get("estimated_members", raw.get("team_size", 0)) or 0),
            "date_added": raw.get("date_added", datetime.now().isoformat(timespec="seconds"))
        }


class MagicbricksLeadSource(LeadSource):
    def __init__(self, api_key: str = None):
        self.logger = Logger("MagicbricksLeadSource")
        self.api_key = api_key or os.getenv("V2_LEAD_SOURCE_API_KEY_REAL_ESTATE", "")
        self.base_url = "https://api.magicbricks.com/v1"

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        if not self.api_key:
            self.logger.warn("Magicbricks API key not configured")
            return []
        self.logger.info(f"Fetching real estate leads from Magicbricks for {location}")
        return []


class NineacresLeadSource(LeadSource):
    def __init__(self, api_key: str = None):
        self.logger = Logger("NineacresLeadSource")
        self.api_key = api_key or os.getenv("V2_LEAD_SOURCE_API_KEY_REAL_ESTATE", "")
        self.base_url = "https://api.99acres.com/v1"

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        if not self.api_key:
            self.logger.warn("99acres API key not configured")
            return []
        self.logger.info(f"Fetching real estate leads from 99acres for {location}")
        return []


class HousingComLeadSource(LeadSource):
    def __init__(self, api_key: str = None):
        self.logger = Logger("HousingComLeadSource")
        self.api_key = api_key or os.getenv("V2_LEAD_SOURCE_API_KEY_REAL_ESTATE", "")
        self.base_url = "https://api.housing.com/v1"

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        if not self.api_key:
            self.logger.warn("Housing.com API key not configured")
            return []
        self.logger.info(f"Fetching real estate leads from Housing.com for {location}")
        return []


class _MultiRealEstateSource(LeadSource):
    def __init__(self, sources: List[LeadSource]):
        self.sources = sources
        self.logger = Logger("MultiRealEstateSource")

    def fetch(self, niche: str, location: str, limit: int) -> List[Dict]:
        combined = []
        for source in self.sources:
            try:
                leads = source.fetch(niche, location, limit)
                combined.extend(leads)
            except Exception as exc:
                self.logger.warn(f"Real estate source failed: {exc}")
        unique = self._deduplicate(combined)
        self.logger.info(f"Fetched {len(unique)} leads from real estate portals")
        return unique[:limit]

    def _deduplicate(self, leads: List[Dict]) -> List[Dict]:
        seen = set()
        merged = []
        for lead in leads:
            key = lead.get("phone") or lead.get("email") or lead.get("id")
            if not key or key in seen:
                continue
            seen.add(key)
            merged.append(lead)
        return merged


class LeadSourceAdapter:
    def __init__(self):
        self.logger = Logger("LeadSourceAdapter")
        self.source_type = settings.LEAD_SOURCE
        self.source_order = settings.LEAD_SOURCE_ORDER
        self.csv_path = settings.LEAD_SOURCE_CSV_PATH
        self.csv_dir = settings.LEAD_SOURCE_CSV_DIR
        self.api_url = settings.LEAD_SOURCE_API_URL
        self.api_key = settings.LEAD_SOURCE_API_KEY
        self.api_url_template = settings.LEAD_SOURCE_API_URL_TEMPLATE

    def fetch_leads(self, niche: str, location: str, limit: int) -> List[Dict]:
        order = self._parse_source_order()
        self.logger.info(f"Using lead source order: {order}")

        if self.source_type == "auto":
            return self._auto_select_source(niche, location, limit)

        if self.source_type in ["csv+api", "api+csv"]:
            combined = []
            for source_name in order:
                leads = self._fetch_from_source(source_name, niche, location, limit)
                combined.extend(leads)

            merged = self._merge_unique_leads(combined)
            if merged:
                return merged[:limit]

            self.logger.info("No leads fetched from configured sources, falling back to mock")
            return MockLeadSource().fetch(niche, location, limit)

        source = self._build_source(self.source_type, niche, location, limit)
        if not source:
            self.logger.warn(f"Unknown source type: {self.source_type}, using mock")
            return MockLeadSource().fetch(niche, location, limit)

        leads = source.fetch(niche, location, limit)
        if not leads:
            self.logger.info("No leads fetched from configured source, falling back to mock")
            leads = MockLeadSource().fetch(niche, location, limit)
        return leads

    def _parse_source_order(self) -> List[str]:
        order = self.source_order.split(",") if self.source_order else []
        cleaned = [item.strip().lower() for item in order if item.strip()]
        return cleaned or ["csv", "api", "mock"]

    def _fetch_from_source(self, source_name: str, niche: str, location: str, limit: int) -> List[Dict]:
        source = self._build_source(source_name, niche, location, limit)
        if not source:
            return []
        leads = source.fetch(niche, location, limit)
        return leads or []

    def _merge_unique_leads(self, leads: List[Dict]) -> List[Dict]:
        unique = {}
        merged = []
        for lead in leads:
            key = lead.get("phone") or lead.get("email") or lead.get("id")
            if not key:
                continue
            if key in unique:
                continue
            unique[key] = True
            merged.append(lead)
        return merged

    def _build_source(self, source_type: str, niche: str, location: str = "", limit: int = 50) -> LeadSource:
        if source_type == "csv":
            csv_path = self._resolve_csv_path(niche)
            return CSVLeadSource(csv_path)
        if source_type == "api":
            api_url, api_key = self._resolve_api_config(niche, location, limit)
            return APILeadSource(api_url, api_key)
        if source_type == "mock":
            return MockLeadSource()
        if source_type == "real_estate":
            api_key = os.getenv("V2_LEAD_SOURCE_API_KEY_REAL_ESTATE", "")
            sources = [
                MagicbricksLeadSource(api_key),
                NineacresLeadSource(api_key),
                HousingComLeadSource(api_key)
            ]
            return _MultiRealEstateSource(sources)
        return None

    def _resolve_csv_path(self, niche: str) -> str:
        if self.csv_path and Path(self.csv_path).exists():
            return self.csv_path

        csv_dir = self.csv_dir or self.csv_path
        if csv_dir and Path(csv_dir).is_dir():
            candidate = Path(csv_dir) / f"{niche}.csv"
            if candidate.exists():
                return str(candidate)
            candidate = Path(csv_dir) / f"{niche}_leads.csv"
            if candidate.exists():
                return str(candidate)

        self.logger.warn(f"No niche-specific CSV lead file found for {niche}")
        return self.csv_path

    def _resolve_api_config(self, niche: str, location: str, limit: int = 50) -> Tuple[str, str]:
        niche_key = niche.upper().replace("-", "_")
        api_url = os.getenv(f"V2_LEAD_SOURCE_API_URL_{niche_key}", self.api_url)
        api_key = os.getenv(f"V2_LEAD_SOURCE_API_KEY_{niche_key}", self.api_key)

        if self.api_url_template:
            api_url = self.api_url_template.format(niche=niche, location=location, limit=limit)

        return api_url, api_key

    def _auto_select_source(self, niche: str, location: str, limit: int) -> List[Dict]:
        sources = ["csv", "api"]
        source_results = {}

        for source_name in sources:
            leads = self._fetch_from_source(source_name, niche, location, limit)
            if leads:
                score = self._score_leads(leads)
                source_results[source_name] = {
                    'leads': leads,
                    'score': score,
                    'count': len(leads)
                }

        if not source_results:
            self.logger.info("Auto source selection found no real leads, falling back to mock")
            return MockLeadSource().fetch(niche, location, limit)

        best_source = max(source_results.items(), key=lambda item: (item[1]['score'], item[1]['count']))
        self.logger.info(f"Auto selected source {best_source[0]} with score {best_source[1]['score']}")
        return best_source[1]['leads'][:limit]

    def _score_leads(self, leads: List[Dict]) -> float:
        total_score = 0
        for lead in leads:
            score = 0
            if lead.get('phone'): score += 2
            if lead.get('email'): score += 1
            if str(lead.get('gmb_status', '')).lower() == 'active': score += 2
            if lead.get('price_range'): score += 1
            if int(str(lead.get('estimated_members', 0)).split()[0] or 0) > 10:
                score += 1
            if lead.get('location') and 'sector' in lead['location'].lower():
                score += 1
            total_score += min(score, 10)
        return round(total_score / len(leads), 1)
