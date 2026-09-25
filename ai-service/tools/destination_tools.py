import os
import serpapi

from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def search_destinations(
        country: str,
        state: str,
        interests: list[str]        
    ):
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI key is not configured")

    client = serpapi.Client(
        api_key=SERPAPI_API_KEY
    )

    interest_query = " ".join(interests)    

    if state:
        query = f"tourist attaraction in {state}, {country}, {interest_query}"
    else:
        query = f"tourist attraction in {country}, {interest_query}"

    results = client.search({
        "engine": "google_maps",
        "q": query,
        "type":"search",
        "hl": "en",
        "gl": "in"
    })

    return results.get("local_results",[])


def filter_destinations(
        destinations: list,
        state: str
    ):
    filtered_destination = []

    for destination in destinations:
        address = destination.get("address","").lower()

        if state and state.lower() not in address:
            continue

        filtered_destination.append(destination)

    return filtered_destination
