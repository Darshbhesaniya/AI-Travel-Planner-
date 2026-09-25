import os
import re
import math
import serpapi
from dotenv import load_dotenv

from llm.llm_client import generate_text

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def resolve_location(location: str):
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY is Not Found")

    client = serpapi.Client(
        api_key=SERPAPI_API_KEY
    )

    results = client.search({
        "engine": "google_maps",
        "q": location,
        "type": "search",
        "hl": "en",
        "gl": "in"
    })

    place_result = results.get("place_results",{})

    if not place_result:
        return None

    gps_coordinates = place_result.get(
        "gps_coordinates",
        {}
    )

    return {
       "name": place_result.get("title"),
       "address": place_result.get("address"),
       "country": place_result.get("country"),
       "latitude": gps_coordinates.get("latitude"),
       "longitude": gps_coordinates.get("longitude")

    }


def resolve_nearby_airports(
        latitude: float,
        longitude: float
        ):
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY is Not Found")

    client = serpapi.Client(
        api_key=SERPAPI_API_KEY
    )

    results = client.search({
        "engine": "google_maps",
        "q": "airports",
        "ll": f"@{latitude},{longitude},12z",
        "type": "search",
        "hl": "en",
        "gl": "in"
    })

    local_results = results.get(
        "local_results",
        []
    )


    airports = []
    seen_airports = set()

    for result in local_results:

        result_types = result.get("types", [])

        # Keep only actual airport listings
        if "Airport" not in result_types:
            continue

        name = result.get("title")

        if not name:
            continue

        normalized_name = name.lower()

        if normalized_name in seen_airports:
            continue

        seen_airports.add(normalized_name)

        gps_coordinates = result.get(
            "gps_coordinates",
            {}
        )

        airport_latitude = gps_coordinates.get("latitude")
        airport_longitude = gps_coordinates.get("longitude")

        if airport_latitude is None or airport_longitude is None:
            continue

        distance_km = calculate_distance(
            latitude,
            longitude,
            airport_latitude,
            airport_longitude
            )

        airports.append({
            "name": name,
            "address": result.get("address"),
            "type": result.get("type"),
            "latitude": gps_coordinates.get("latitude"),
            "longitude": gps_coordinates.get("longitude"),
            "distance_km": round(distance_km, 2)
        })

        nearby_airports = [
            airport
            for airport in airports
            if airport["distance_km"] <= 100
            ]

    return nearby_airports

def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
):
    earth_radius_km = 6371

    latitude1 = math.radians(latitude1)
    longitude1 = math.radians(longitude1)
    latitude2 = math.radians(latitude2)
    longitude2 = math.radians(longitude2)

    delta_latitude = latitude2 - latitude1
    delta_longitude = longitude2 - longitude1

    a = (
        math.sin(delta_latitude / 2) ** 2
        + math.cos(latitude1)
        * math.cos(latitude2)
        * math.sin(delta_longitude / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius_km * c

