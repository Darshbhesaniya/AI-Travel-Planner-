from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm.llm_client import test_llm
from routers import meta,trip

app = FastAPI(title="AI Travel Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(meta.router)
app.include_router(trip.router)


@app.get("/hello")
def hello():
    return {
        "message": "Hello From Python AI Service"
    }

@app.get("/test-llm")
def test_llm_endpoint():
    result = test_llm()

    return{
        "response": result
    }