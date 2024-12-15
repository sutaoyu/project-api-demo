from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic.generics import GenericModel
from sqlalchemy.orm import Session
from typing import Any, Generic, List, Optional, TypeVar
from app import crud, models, schemas
from app.api import deps
from app.schemas.base import ResponseModel, MultiResponseModel
from app.utils import page_data_list

router = APIRouter()


def to_dict_list(objects):
    return [obj.__dict__ for obj in objects]


@router.post("/create/{rule_id}", response_model=ResponseModel[schemas.Clue])
def create_clue(
    *,
    db: Session = Depends(deps.get_db),
    clue: schemas.ClueCreate,
    rule_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new clue.
    """
    topic = "topic_demo"
    clue = crud.clue.create_one_with_rule(
        db=db, obj_in=clue, rule_id=rule_id, topic=topic
    )
    return ResponseModel(code=200, msg="ok", data=clue)


@router.get("/{clue_id}", response_model=ResponseModel[schemas.Clue])
def read_clue(
    *,
    clue_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch a single clue by ID
    """
    clue = crud.clue.get_by_clue_id(db, clue_id=clue_id)
    if not clue:
        raise HTTPException(status_code=404, detail=f"clue with ID {clue_id} not found")
    return ResponseModel(code=200, msg="ok", data=clue)


@router.delete("/{clue_id}", response_model=ResponseModel[schemas.Clue])
def delete_clue(
    *,
    db: Session = Depends(deps.get_db),
    clue_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a single clue by ID
    """
    clue = crud.clue.get_by_clue_id(db, clue_id=clue_id)
    if not clue:
        raise HTTPException(status_code=404, detail=f"clue with ID {clue_id} not found")
    clue = crud.clue.delete_by_clue_id(db=db, clue_id=clue_id)
    return ResponseModel(code=200, msg="ok", data=clue)
