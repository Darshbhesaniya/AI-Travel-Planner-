import json
from datetime import datetime

from graph.state import TravelState
from llm.llm_client import generate_structured

def finalizer_agent(state: TravelState):
    destination = state["selected_destination"]
    flight = state["selected_flight"]
    hotel = state["selected_hotel"]
    travelers = state["travelers"]

    start_date = state["start_date"]
    end_date = state["end_date"]


    duration_days = (
        datetime.strptime(end_date, "%d-%m-%Y")
        - datetime.strptime(start_date, "%d-%m-%Y")
    ).days

    flight_total = flight["price"] * travelers
    hotel_total = hotel["total_price"]
    grand_total = flight_total + hotel_total
    budget = state["budget"]

    trip_info = {
        "origin": state["origin_city"],
        "destination": f'{destination["name"]}, {state["allowed_state"]}',
        "start_date": start_date,
        "end_date": end_date,
        "duration_days": duration_days,
        "travelers": travelers
    }

    flight_data = {
        "airline": flight["airline"],
        "trip_type": flight["trip_type"],
        "stops": flight["stops"],
        "departure_time": flight["departure_time"],
        "arrival_time": flight["arrival_time"],
        "duration_minutes": flight["total_duration_minutes"],
        "price_per_person": flight["price"],
        "total_price": flight_total
    }

    hotel_data = {
        "name": hotel["name"],
        "hotel_class": hotel["hotel_class"],
        "rating": hotel["overall_rating"],
        "price_per_night": hotel["price_per_night"],
        "total_price": hotel_total,
        "amenities": hotel["amenities"]
    }

    cost_breakdown = {
        "flight_total": flight_total,
        "hotel_total": hotel_total,
        "grand_total": grand_total,
        "budget": budget,
        "remaining_budget": budget - grand_total,
        "within_budget": grand_total <= budget
    }

    prompt = f"""
        You are a travel assistant writing the final summary of a booked trip.

        TRIP DATA (all number are final and already correct, do not change them):

        Trip: {json.dumps(trip_info, indent=2)}
        Flight: {json.dumps(flight_data, indent=2)}
        Hotel: {json.dumps(hotel_data, indent=2)}
        Cost: {json.dumps(cost_breakdown,indent=2)}
        Interest: {", ".join(state["interests"])}

        Your task:
    1. Write a short, catchy trip_title (5-8 words).
    2. Write a 2-3 sentence overview of the trip, mentioning the destination and matching the traveller's interests.
    3. Write a 1-sentence flight_highlight (why this flight is a good pick).
    4. Write a 1-sentence hotel_highlight (why this hotel is a good pick).
    5. Write exactly 3 short, practical travel tips for this destination and season.
    """

    
    schema = {
        "type": "object",
        "properties": {
            "trip_title": {"type": "string"},
            "overview": {"type": "string"},
            "flight_highlight": {"type": "string"},
            "hotel_highlight": {"type": "string"},
            "tips": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 3
            }
        },
        "required": ["trip_title", "overview", "flight_highlight", "hotel_highlight", "tips"],
        "additionalProperties": False
    }

    llm_response = generate_structured(
        prompt=prompt,
        schema_name="final_trip_summary",
        schema=schema
    )

    llm_result = json.loads(llm_response)

    flight_data["highlight"] = llm_result["flight_highlight"]
    hotel_data["highlight"] = llm_result["hotel_highlight"]

    final_plan = {
        "trip_title": llm_result["trip_title"],
        "overview": llm_result["overview"],
        "trip_info": trip_info,
        "flight": flight_data,
        "hotel": hotel_data,
        "cost_breakdown": cost_breakdown,
        "tips": llm_result["tips"]
    }

    return {"final_plan": final_plan}

    