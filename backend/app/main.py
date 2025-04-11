from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router

app = FastAPI(title="Investment Strategies API")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
