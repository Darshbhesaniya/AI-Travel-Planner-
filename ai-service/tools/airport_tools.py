import json

from pathlib import Path

from utils.state_code import STATE_REGION_CODES

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "airports_india.json"

with open(DATA_FILE, encoding="utf-8") as f:
    AIRPORTS = json.load(f)

AIRPORTS_BY_CODE = {airport["iata_code"]: airport for airport in AIRPORTS }



def get_origin_options():
    """Get Airport Options for the UI dropdown as {city: iata_code}. """
    return dict(sorted(
        (airport["municipality"], airport["iata_code"])
        for airport in AIRPORTS
    ))

def get_airport(code: str):
    """Return the airport dictionary if the IATA code is valid, otherwise None"""
    if not code:
        return None

    return AIRPORTS_BY_CODE.get(code.strip().upper())

def get_destination_candidates(state_name: str = None):
    """Return all airports except the origin airport."""
    airports = AIRPORTS

    if state_name:
        region = STATE_REGION_CODES.get(state_name)

        if region:
            airports = [airport for airport in AIRPORTS if airport["iso_region"] == region ]

    return sorted(airports, key=lambda a: a["iata_code"])