from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskQuery
from app.utils import generate_id


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TaskCreate, owner_user_id: str
    ) -> Task:
        obj_in_data = jsonable_encoder(obj_in)
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj_in_data["task_id"] = generate_id()
        obj_in_data["owner_user_id"] = owner_user_id
        obj_in_data["status"] = 0
        db_obj = self.model(**obj_in_data, create_time=now_time, update_time=now_time)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_task_id(self, db: Session, *, task_id: str) -> Task:
        return db.query(self.model).filter(self.model.task_id == task_id).first()

    def get_by_user_id(self, db: Session, *, owner_user_id: str) -> Task:
        return (
            db.query(self.model)
            .filter(self.model.owner_user_id == owner_user_id)
            .first()
        )

    def get_by_task_name_and_user(
        self, db: Session, *, task_name: str, owner_user_id: str
    ) -> Task:
        return (
            db.query(self.model)
            .filter(
                and_(
                    self.model.task_name == task_name,
                    self.model.owner_user_id == owner_user_id,
                )
            )
            .first()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.owner_user_id == owner_user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def query_task_multi(
        self,
        db: Session,
        *,
        query: TaskQuery,
        owner_user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        filter_conditions = [
            or_(
                self.model.task_name.ilike(f"%{query.keywords}%"),
                self.model.source.ilike(f"%{query.keywords}%"),
                self.model.description.ilike(f"%{query.keywords}%"),
            ),
            or_(self.model.type == query.type, query.type == None),
            or_(self.model.status == int(query.status), int(query.status) == -1),
            self.model.create_time.between(query.start_time, query.end_time),
            Task.owner_user_id == owner_user_id,
        ]

        if query.sort == "desc":
            order_by = self.model.create_time.desc()
        else:
            order_by = self.model.create_time.asc()

        result_list = (
            db.query(self.model)
            .filter(and_(*filter_conditions))
            .order_by(order_by)
            .limit(limit)
            .offset(skip)
            .all()
        )
        return result_list

    def update_field(self, db: Session, *, data: dict, task_id: str) -> Task:
        db_obj = db.query(self.model).filter(self.model.task_id == task_id).first()
        db_obj_json = jsonable_encoder(db_obj)
        for field in db_obj_json:
            if field in data:
                setattr(db_obj, field, data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_by_task_id(self, db: Session, *, task_id: str) -> Task:
        obj = db.query(self.model).filter(self.model.task_id == task_id).first()
        db.delete(obj)
        db.commit()
        return obj

    def query_multi_by_task_id_list(
        self, db: Session, *, task_id_list: List[str]
    ) -> List[Task]:
        result_list = (
            db.query(self.model).filter(self.model.task_id.in_(task_id_list)).all()
        )
        return result_list


task = CRUDTask(Task)
