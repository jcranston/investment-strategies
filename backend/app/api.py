from fastapi import APIRouter
from pydantic import BaseModel

from app.strategies import daily, rolling

router = APIRouter()


class SimulationRequest(BaseModel):
    strategy: str
    start_date: str
    end_date: str
    tickers: list[str]


@router.post("/simulate")
def simulate(request: SimulationRequest):
    if request.strategy == "daily":
        return daily.simulate_daily(
            request.start_date, request.end_date, request.tickers
        )
    elif request.strategy == "rolling":
        return rolling.simulate_rolling(
            request.start_date, request.end_date, request.tickers
        )
    else:
        return {"error": "Unknown strategy"}
