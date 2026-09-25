from graph.state import TravelState

def supervisor_node(state: TravelState):
    completed_agent = state["completed_agents"]

    if "destination" not in completed_agent:
        next_agent = "destination"

    elif "flight" not in completed_agent:
        next_agent = "flight"

    elif "hotel" not in completed_agent:
        next_agent = "hotel"

    else:
        next_agent = "finalizer"

    return {
        "next_agent": next_agent
    }