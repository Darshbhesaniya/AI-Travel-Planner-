import uuid
from fastapi import FastAPI
from langgraph.types import Command
from graph.travel_graph import travel_graph
from llm.llm_client import test_llm


app = FastAPI()

@app.get("/hello")
def hello():
    return {
        "message": "Hello From Python AI Service"
    }

@app.get("/run-graph")
def run_graph():
    thread_id = str(uuid.uuid4())

    initial_state = {
     "origin_city": "Ahmedabad",
     "origin_airport": "AMD",
     "budget": 150000,
     "currency": "INR",
     "start_date": "30-09-2026",
     "end_date": "07-10-2026",
     "travelers": 2,
     "interests": ["beach","food","nature"],

    "allowed_country": "India",
    "allowed_state": "Goa",

     "destination_options":[],
     "selected_destination": {},

     "flight_options": [],
     "selected_flight": {},

     "hotel_options": [],
     "selected_hotel": {},

     "next_agent": "",
     "completed_agents": [],

     "final_plan": {},

     "errors": []
    }

    config = {
        "configurable":{
            "thread_id": thread_id
        }
    }

    result = travel_graph.invoke(
        initial_state,
        config=config
        )
    result["thread_id"] = thread_id
    return result


@app.post("/select-destination")
def select_destination(thread_id: str, destination: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = travel_graph.invoke(
        Command(resume=destination),
        config=config
    )

    return result

@app.post("/select-flight")
def select_flight(thread_id: str, flight_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    result = travel_graph.invoke(
        Command(resume=flight_id),
        config=config
    )

    return result

@app.post("/select-hotel")
def select_hotel(thread_id: str, hotel_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    result = travel_graph.invoke(
        Command(resume=hotel_id),
        config=config
    )

    return result

@app.get("/test-llm")
def test_llm_endpoint():
    result = test_llm()

    return{
        "response": result
    }