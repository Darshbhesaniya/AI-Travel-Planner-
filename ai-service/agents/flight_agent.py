import json
from langgraph.types import interrupt

from graph.state import TravelState
from llm.llm_client import generate_structured
from tools.flight_tools import search_flights

def flight_agent(state: TravelState):

    origin_airport = state["origin_airport"]
    destination_airport = state["selected_destination"]["airport_code"]


    flights = search_flights(
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        outbound_date=state["start_date"],
        return_date=state["end_date"],
        currency=state["currency"]
    )

    if not flights:
        return {"errors": [f"No flights found from {origin_airport} to {destination_airport}"]}

    indexed_flights = []

    for i, flight in enumerate(flights):
        indexed_flights.append({"flight_id": f"F{i+1}", **flight})

    flight_id_enum = [f["flight_id"] for f in indexed_flights]

    flight_list_text = "\n".join(
        f'{f["flight_id"]} | {f["airline"]} | Price: {f["price"]} | '
        f'Stops: {f["stops"]} | Duration: {f["total_duration_minutes"]} min |'
        f'Departs: {f["departure_time"]} | Arrives: {f["arrival_time"]}'
        for f in indexed_flights
    )

    prompt = f"""You are a flight recommendation assistant.
        TRAVELLER DETAILS:
        Total trip budget: {state["budget"]} {state["currency"]}
        Travellers: {state["travelers"]}

        AVAILABLE FLIGHTS (format: flight_id | airline | price | stops | duration | departure | arrival):

        {flight_list_text}

        RULES:
        1. Recommend exactly 3 flights (fewer if less than 3 are available) from the list above.
        2. Use only flight_id values from the list. Never invent one.
        3. Prefer a good balance of price, duration and fewer stops.
        4. Keep total flight cost (for all travellers) reasonable within the overall trip budget.
        5. "reason" must be 1-2 sentences explaining the trade-off (price vs duration vs stops).
    """

    schema = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "flight_id": {
                            "type": "string",
                            "enum": flight_id_enum
                        },
                        "reason": {"type": "string"}
                    },
                    "required": ["flight_id", "reason"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False
    }

    llm_response = generate_structured(
        prompt=prompt,
        schema_name="flight_recommendations",
        schema=schema
    )

    result = json.loads(llm_response)

    flights_by_id = {f["flight_id"]: f for f in indexed_flights}

    recommendations = []
    seen = set()
    for rec in result["recommendations"]:
        flight = flights_by_id.get(rec["flight_id"])
        if not flight or flight["flight_id"] in seen:
            continue
        seen.add(flight["flight_id"])
        recommendations.append({**flight, "reason": rec["reason"]})

    if not recommendations:
        return {"errors": ["No valid flight recommendation found"]}

    return {"flight_options": recommendations}



def flight_selection(state: TravelState):
    user_selection = interrupt({
        "type": "flight_selection",
        "message": "Please select your flight",
        "options": state["flight_options"]
    })

    selected_flight = next(
        flight for flight in state["flight_options"]
        if flight["flight_id"] == user_selection
    )

    return {
        "selected_flight": selected_flight,
        "completed_agents": [*state["completed_agents"], "flight"]
    }

    

    