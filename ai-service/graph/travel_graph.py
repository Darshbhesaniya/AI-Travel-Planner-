from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import TravelState
from agents.supervisor import supervisor_node
from agents.destination_agent import destination_agent,destination_selection
from agents.flight_agent import flight_agent,flight_selection
from agents.hotel_agent import hotel_agent,hotel_selection
from agents.finalizer_agent import finalizer_agent

def route_next_agent(state: TravelState):
    return state["next_agent"]


graph_builder = StateGraph(TravelState)

graph_builder.add_node("supervisor", supervisor_node)

graph_builder.add_node("destination", destination_agent)
graph_builder.add_node("destination_selection", destination_selection)

graph_builder.add_node("flight", flight_agent)
graph_builder.add_node("flight_selection", flight_selection)

graph_builder.add_node("hotel", hotel_agent)
graph_builder.add_node("hotel_selection",hotel_selection)

graph_builder.add_node("finalizer", finalizer_agent)



graph_builder.add_edge(START, "supervisor")

graph_builder.add_conditional_edges(
    "supervisor",
    route_next_agent,
    {
        "destination": "destination",
        "flight": "flight",
        "hotel": "hotel",
        "finalizer": "finalizer"
    }
)

graph_builder.add_edge("destination", "destination_selection")
graph_builder.add_edge("destination_selection","supervisor")
graph_builder.add_edge("flight", "flight_selection")
graph_builder.add_edge("flight_selection","supervisor")
graph_builder.add_edge("hotel","hotel_selection")
graph_builder.add_edge("hotel_selection","supervisor")


graph_builder.add_edge("finalizer",END)


checkpointer = MemorySaver()

travel_graph = graph_builder.compile(
    checkpointer=checkpointer
)