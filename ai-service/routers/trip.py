import uuid

from fastapi import APIRouter
from langgraph.types import Command

from graph.travel_graph import travel_graph
from schema.trip import TripRequest
from tools.airport_tools import get_airport

router = APIRouter(tags=["trip"])

def _config(thread_id: str):
    return {
        "configurable": {"thread_id": thread_id}
    }

def _resume(thread_id: str, value: str):
    return travel_graph.invoke(Command(resume=value), config=_config(thread_id))



@router.post("/start-trip")
def start_trip(req: TripRequest):
    airport = get_airport(req.origin_airport)
    thread_id = str(uuid.uuid4())

    initial_state = {
        "origin_city": airport["municipality"],
        "origin_airport": airport["iata_code"],
        "budget": req.budget,       
        "currency": req.currency,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "travelers": req.travelers,
        "interests": req.interests,
        "allowed_country": "India",
        "allowed_state": req.allowed_state,
        "destination_options": [],
        "selected_destination": {},
        "flight_options": [],
        "selected_flight": {},
        "hotel_options": [],
        "selected_hotel": {},
        "next_agent": "",
        "completed_agents": [],
        "final_plan": {},
        "errors": [],
    }

    result = travel_graph.invoke(initial_state, config=_config(thread_id))
    result["thread_id"] = thread_id
    return result


@router.post("/select-destination")
def select_destination(thread_id: str,destination: str):
    return _resume(thread_id, destination)

@router.post("/select-flight")
def select_flight(thread_id: str, flight_id: str):
    return _resume(thread_id, flight_id)

@router.post("/select-hotel")
def select_hotel(thread_id: str, hotel_id: str):
    return _resume(thread_id,hotel_id)

