from typing import TypedDict

class TravelState(TypedDict):
    origin_city: str
    origin_airport: str
    budget: float
    currency: str
    start_date: str
    end_date: str
    travelers: int
    interests: list[str]

    allowed_country: str
    allowed_state: str

    destination_options:list
    selected_destination: dict

    flight_options: list
    selected_flight: dict

    hotel_options: list
    selected_hotel: dict

    next_agent: str
    completed_agents: list[str]

    final_plan:dict

    errors: list[str]
