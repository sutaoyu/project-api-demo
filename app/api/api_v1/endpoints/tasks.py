from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any
from datetime import datetime
from app import crud, models, schemas
from app.api import deps
from app.utils import page_data_list
from app.schemas.base import ResponseModel, MultiResponseModel

router = APIRouter()


@router.post("/create", response_model=ResponseModel[schemas.Task])
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task.
    """
    old_task = crud.task.get_by_task_name_and_user(
        db, task_name=task.task_name, owner_user_id=current_user.user_id
    )
    if old_task:
        raise HTTPException(
            status_code=400,
            detail="The user's task with this task_name already exists in the system",
        )
    new_task = crud.task.create_with_owner(
        db=db, obj_in=task, owner_user_id=current_user.user_id
    )
    return ResponseModel(code=200, msg="ok", data=new_task)


@router.post("/query", response_model=ResponseModel[MultiResponseModel[schemas.Task]])
def query_task_multi(
    *,
    db: Session = Depends(deps.get_db),
    query: schemas.TaskQuery,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    query a list of task
    """
    result = crud.task.query_task_multi(
        db, query=query, owner_user_id=current_user.user_id
    )
    total_page, total_count, final_items = page_data_list(
        result, query.page_no, query.page_size
    )
    data = {"data_list": final_items, "pages": total_page, "total": total_count}
    return ResponseModel(code=200, msg="ok", data=data)


@router.get("/{task_id}", response_model=ResponseModel[schemas.Task])
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch a single task by ID
    """
    task = crud.task.get_by_task_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with ID {task_id} not found")
    if not crud.user.is_admin(current_user) and (
        task.owner_user_id != current_user.user_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return ResponseModel(code=200, msg="ok", data=task)


@router.put("/{task_id}", response_model=ResponseModel[schemas.Task])
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a single task by ID
    """
    task = crud.task.get_by_task_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with ID {task_id} not found")
    if not crud.user.is_admin(current_user) and (
        task.owner_user_id != current_user.user_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return ResponseModel(code=200, msg="ok", data=task)


@router.delete("/{task_id}", response_model=ResponseModel[schemas.Task])
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch a single task by ID
    """
    task = crud.task.get_by_task_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with ID {task_id} not found")
    if not crud.user.is_admin(current_user) and (
        task.owner_user_id != current_user.user_id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = crud.task.delete_by_task_id(db=db, task_id=task_id)
    return ResponseModel(code=200, msg="ok", data=task)
