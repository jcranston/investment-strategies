from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.strategies.daily import simulate_daily
from app.strategies.rolling import simulate_rolling

app = FastAPI(title="Investment Strategies API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    strategy: str
    tickers: List[str]
    start_date: str
    end_date: str
    initial_value: float = 1000000  # optional, with default


@app.post("/simulate")
def simulate(request: SimulationRequest):
    if request.strategy == "daily":
        return simulate_daily(request.start_date, request.end_date, request.tickers)
    elif request.strategy == "rolling":
        return simulate_rolling(
            request.start_date, request.end_date, request.tickers, request.initial_value
        )
    else:
        return {"error": f"Unknown strategy: {request.strategy}"}
