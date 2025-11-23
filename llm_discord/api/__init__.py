import logging
from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/health")
async def health_check():
    return {"detail": "healthy"}


@api.get("/ready")
async def readiness_check():
    return {"detail": "ready"}
