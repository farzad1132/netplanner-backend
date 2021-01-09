from fastapi import APIRouter, Depends


project_router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)