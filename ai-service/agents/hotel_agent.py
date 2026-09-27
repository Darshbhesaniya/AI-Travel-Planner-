import json

from langgraph.types import interrupt

from graph.state import TravelState
from llm.llm_client import generate_structured
from tools.hotel_tools import search_hotels

def hotel_agent(state: TravelState):

    destination_city = state["selected_destination"]["name"]

    hotels = search_hotels(
        destination_city=destination_city,
        check_in_date = state["start_date"],
        check_out_date = state["end_date"],
        adults=state["travelers"],
        currency=state["currency"]
    )

    if not hotels:
        return {"errors": [f"No hotels Found in {destination_city}"]}

    indexed_hotels = []

    for i,hotel in enumerate(hotels):
        indexed_hotels.append({"hotel_id": f"H{i+1}", **hotel})

    hotel_id_enum = [h["hotel_id"] for h in indexed_hotels]

    hotel_list_text = "\n".join(
        f'{h["hotel_id"]} | {h["name"]} | Class: {h["hotel_class"]}-star | '
        f'Rating: {h["overall_rating"]} ({h["reviews"]} reviews) | '
        f'Total price: {h["total_price"]} | Amenities: {", ".join(h["amenities"])}'
        for h in indexed_hotels
    )


    prompt = f"""You are a hotel recommendation assistant.

    TRAVELLER DETAILS:
    Destination: {destination_city}
    Total trip budget: {state["budget"]} {state["currency"]} (covers flights + hotel + everything)
    Travellers: {state["travelers"]}
    Interests: {", ".join(state["interests"])}

    AVAILABLE HOTELS (format: hotel_id | name | class | rating | total price for the whole stay | amenities):

    {hotel_list_text}

    RULES:
    1. Recommend exactly 3 hotels (fewer if less than 3 are available) from the list above.
    2. Use only hotel_id values from the list. Never invent one.
    3. Prefer a good balance of price, rating and amenities relevant to the traveller's interests.
    4. Keep total hotel cost reasonable within the overall trip budget.
    5. "reason" must be 1-2 sentences explaining why this hotel is a good fit.
    """

    schema = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {
                            "type": "string",
                            "enum": hotel_id_enum
                        },
                        "reason": {"type": "string"}
                    },
                    "required": ["hotel_id", "reason"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False
    }


    llm_response = generate_structured(
        prompt=prompt,
        schema_name="hotel_recommendations",
        schema=schema
    )

    result = json.loads(llm_response)

    hotels_by_id = {h["hotel_id"]: h for h in indexed_hotels}

    recommendations = []
    seen = set()

    for rec in result["recommendations"]:
        hotel = hotels_by_id.get(rec["hotel_id"])

        if not hotel or hotel["hotel_id"] in seen:
            continue

        seen.add(hotel["hotel_id"])
        recommendations.append({**hotel, "reason": rec["reason"]})

    if not recommendations:
        return {"errors": ["No valid hotel recommendation Found"]}

    return {"hotel_options": recommendations}

def hotel_selection(state: TravelState):
    user_selection = interrupt({
        "type": "hotel_selection",
        "message": "Please select your hotel",
        "options": state["hotel_options"]
    })

    selected_hotel = next(
        hotel for hotel in state["hotel_options"]
        if hotel["hotel_id"] == user_selection
    )

    return {
        "selected_hotel": selected_hotel,
        "completed_agents":[*state["completed_agents"], "hotel"]
    }

