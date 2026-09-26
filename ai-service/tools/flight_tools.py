import os
from datetime import datetime

import serpapi
from dotenv import load_dotenv


load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def convert_date(date_str: str) -> str:
    """DD-MM-YYYY -> YYYY-MM-DD"""
    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

def search_flights(
        origin_airport: str,
        destination_airport: str,
        outbound_date: str,
        return_date: str,
        currency: str = "INR"
    ):
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY is not configured")

    client = serpapi.Client(api_key=SERPAPI_API_KEY)

    results = client.search({
        "engine": "google_flights",
        "departure_id": origin_airport,
        "arrival_id": destination_airport,
        "outbound_date": convert_date(outbound_date),
        "return_date": convert_date(return_date),
        "currency": currency,
        "hl": "en"
    })

    raw_flights = results.get("best_flights",[]) + results.get("other_flights",[])

    simplified = []

    for flight in raw_flights:
        legs = flight.get("flights", [])

        if not legs:
            continue

        first_leg = legs[0]
        last_leg = legs[-1]

        simplified.append({
            "airline": first_leg.get("airline"),
            "price": flight.get("price"),
            "trip_type": flight.get("type"),
            "total_duration_minutes": flight.get("total_duration"),
            "stops": len(legs) - 1,
            "departure_airport": first_leg.get("departure_airport", {}).get("id"),
            "departure_time": first_leg.get("departure_airport",{}).get("time"),
            "arrival_airport": last_leg.get("arrival_airport",{}).get("id"),
            "arrival_time": last_leg.get("arrival_airport",{}).get("time"),
    
        })

    return simplified


