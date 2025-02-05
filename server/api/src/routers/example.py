from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params
from src.repository import SportsRepository
from src.models.models import Sport, SportCreateModel, SportOut
import typing

router = APIRouter(
    prefix="/api/sports",
    tags=["Sports CRUD"],
)

@router.get("/", response_model=Page[SportOut])
async def get_sports(params: Params = Depends()):
    page = SportsRepository.getAllSports(params)
    return page

@router.get("/{id}")
async def get_sport_by_id(id: int):
    sport = SportsRepository.getSportById(id)
    return sport

@router.post("/")
async def create_sport(sport: SportCreateModel):
    sport = SportsRepository.createSport(Sport(**sport.model_dump()))
    return sport

@router.put("/{id}")
async def update_sport(id: int, sport: SportOut):
    sport = SportsRepository.updateSport(id, sport)
    return sport

@router.delete("/{id}")
async def delete_sport(id: int):
    result = SportsRepository.deleteSportById(id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Sport not found")

    return {"message" : "Sport delete success"}