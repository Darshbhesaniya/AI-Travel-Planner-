import os
from datetime import datetime

import serpapi
from dotenv import load_dotenv

from tools.flight_tools import convert_date

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def search_hotels(
        destination_city: str,
        check_in_date: str,
        check_out_date: str,
        adults: int = 2,
        currency: str = "INR"
    ):
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY is not configured")

    client = serpapi.Client(api_key=SERPAPI_API_KEY)

    results = client.search({
        "engine": "google_hotels",
        "q": f"{destination_city} hotels",
        "check_in_date": convert_date(check_in_date),
        "check_out_date": convert_date(check_out_date),
        "adults": adults,
        "currency": currency,
        "gl": "in",
        "hl": "en"
    })

    properties = results.get("properties", [])

    simplified = []

    for property in properties:
        if property.get("type") != "hotel":
            continue

        total_rate = property.get("total_rate") or {}
        rate_per_night = property.get("rate_per_night") or {}

        total_price = total_rate.get("extracted_lowest")

        if total_price is None:
            continue

        simplified.append({
            "name": property.get("name"),
            "hotel_class": property.get("extracted_hotel_class"),
            "overall_rating": property.get("overall_rating"),
            "reviews": property.get("reviews"),
            "price_per_night": rate_per_night.get("extracted_lowest"),
            "total_price": total_price,
            "amenities": property.get("amenities", [])[:5],
            "link": property.get("link")
        })

    return simplified