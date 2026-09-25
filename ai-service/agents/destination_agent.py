import json

from langgraph.types import interrupt

from graph.state import TravelState
from llm.llm_client import generate_structured
from tools.airport_tools import get_airport,get_destination_candidates


def destination_agent(state: TravelState):

    country = state["allowed_country"]
    state_name = state["allowed_state"]
    interest = state["interests"]

    candidates = get_destination_candidates(state["allowed_state"])

    airport_list = "\n".join(
        f'{airport["iata_code"]} | {airport["municipality"]} | {airport["iso_region"]} | {airport["name"]}'
        for airport in candidates
    )

    static_part = f"""You are an expert Indian Travel destination recommendar.

    ALLOWED AIRPORTS (format: IATA code | city).
    You may ONLY choose destinations from this list:
    {airport_list}

    RULES:
    1. Choose exactly 3 DIFFERENT airports from the allowed list.
    2. Use only IATA codes that appear in the list. Never invent a code.
    3. Rank by how well the city fits the traveller's interests, travel dates (season/weather) and budget.
    4. Prefer variety: the 3 picks should offer different experiences, not three near-identical places.
    5. Never pick the traveller's origin airport.
    6. Judge budget only by general affordability of the destination for the group size and trip length.
    Do not invent prices, flight fares or availability.
    7. "reason" must be 1-2 sentences, mention which of the traveller's interests the city matches,
    and why it suits the season and budget. Be specific and concrete, not generic.
    """

    dynamic_part = f""" 
                TRAVELLER DETAILS:
    Origin: {state["origin_city"]} ({state["origin_airport"]})
    Interests: {", ".join(state["interests"])}
    Budget: {state["budget"]} {state["currency"]} in total
    Travellers: {state["travelers"]}
    Dates: {state["start_date"]} to {state["end_date"]}

    Recommend the 3 best destinations now.    
    """

    prompt = static_part + dynamic_part

    schema = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "airport_code": {
                            "type": "string",
                            "enum": [airport["iata_code"] for airport in candidates]
                        },
                        "reason": {"type": "string"}
                    },
                    "required": ["airport_code", "reason"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False
    }

    llm_response = generate_structured(
        prompt=prompt,
        schema_name="destination_recommendations",
        schema=schema
    )

    result = json.loads(llm_response)

    recommendations = []
    seen = set()

    for recommendation in result["recommendations"]:
        airport = get_airport(recommendation["airport_code"])

        if not airport or airport["iata_code"] in seen:
            continue

        seen.add(airport["iata_code"])
        recommendations.append({
            "name": airport["municipality"],
            "reason": recommendation["reason"],
            "airport_code": airport["iata_code"],
            "airport_name": airport["name"]
        })

    if not recommendations:
            return {
            "errors": ["No Valid destination with airport Found"]
        }

    return {"destination_options": recommendations}

def destination_selection(state: TravelState):
     user_selection = interrupt({
        "type": "destination_selection",
        "message": "Please Select your destination",
        "options": state["destination_options"]
     })

     selected_destination = next(
          destination for destination in state["destination_options"]
          if destination["name"] == user_selection
     )
    
    
     return {
          "selected_destination": selected_destination,
          "completed_agents": [*state["completed_agents"], "destination"]
     }