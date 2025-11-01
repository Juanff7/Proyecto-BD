from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import cargo as Crud_Cargo
from src.schemas import cargo as Schema_cargo

router = APIRouter()



@router.post("/Create/Cargo", response_model=Schema_cargo.Cargoout)
def Created_cargo(cargo: Schema_cargo.CargoCreate , db: Session = Depends(get_db)):
    return Crud_Cargo.Created_cargo(db = db , data= cargo)