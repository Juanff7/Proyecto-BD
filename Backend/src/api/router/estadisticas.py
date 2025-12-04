from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.debs import get_db
from src.crud.estadistica import get_dashboard_data

router = APIRouter(prefix="/Dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data(db)
