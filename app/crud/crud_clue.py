from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.clue import Clue
from app.schemas.clue import (
    ClueCreate,
    ClueUpdate,
    ClueQuery,
    ClueIsFavorite,
    ClueIsFavoriteQuery,
    ClueQueryBase,
)
from app.schemas.base import TopicType
from app.utils import generate_id


class CRUDClue(CRUDBase[Clue, ClueCreate, ClueUpdate]):
    def create_one_with_rule(
        self, db: Session, *, obj_in: ClueCreate, rule_id: str, topic: TopicType
    ) -> Clue:
        obj_in_data = jsonable_encoder(obj_in)
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj_in_data["clue_id"] = generate_id()
        db_obj = self.model(
            **obj_in_data,
            rule_id=rule_id,
            topic=topic,
            create_time=now_time,
            update_time=now_time,
            origin_create_time=now_time,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_clue_id(self, db: Session, *, clue_id: str) -> Clue:
        return db.query(self.model).filter(self.model.clue_id == clue_id).first()

    def get_by_rule_id(self, db: Session, *, rule_id: str) -> Clue:
        return db.query(self.model).filter(self.model.rule_id == rule_id).first()

    def get_clue_list_by_rule_id(self, db: Session, *, rule_id: str) -> List[Clue]:
        return db.query(self.model).filter(self.model.rule_id == rule_id).all()

    def get_clue_list_by_clue_id_list_no_sort(
        self, db: Session, *, clue_id_list: List[str]
    ):
        return db.query(self.model).filter(self.model.clue_id.in_(clue_id_list)).all()

    def get_clue_list_by_document_id(
        self, db: Session, *, document_id: str
    ) -> List[Clue]:
        return db.query(self.model).filter(self.model.document_id == document_id).all()

    def get_clue_list_by_clue_id_list(
        self,
        db: Session,
        *,
        clue_id_list: List[str],
        query: ClueQueryBase,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Clue]:
        filter_conditions = [
            getattr(self.model, query.time_span_item, "create_time").between(
                query.start_time, query.end_time
            ),
            self.model.clue_id.in_(clue_id_list),
        ]

        # 根据给定的排序选项进行排序，默认按照线索推荐时间进行排序
        if query.sort == "desc":
            order_by = getattr(self.model, query.sort_item, "create_time").desc()
        else:
            order_by = getattr(self.model, query.sort_item, "create_time").asc()

        if limit == -1:
            return (
                db.query(self.model)
                .filter(and_(*filter_conditions))
                .order_by(order_by)
                .offset(skip)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .filter(and_(*filter_conditions))
                .order_by(order_by)
                .limit(limit)
                .offset(skip)
                .all()
            )

    def query_by_clue_id_list(
        self, db: Session, *, clue_id_list: List[str]
    ) -> List[Clue]:
        result_list = (
            db.query(self.model).filter(self.model.clue_id.in_(clue_id_list)).all()
        )
        return result_list

    # 根据document_id返回is_favorite状态
    def get_clue_list_by_document_id_list(
        self,
        db: Session,
        *,
        document_id_list: List[str],
        skip: int = 0,
        limit: int = 100,
    ) -> List[Clue]:
        filter_conditions = [self.model.document_id.in_(document_id_list)]

        if limit == -1:
            return (
                db.query(self.model).filter(and_(*filter_conditions)).offset(skip).all()
            )
        else:
            return (
                db.query(self.model)
                .filter(and_(*filter_conditions))
                .limit(limit)
                .offset(skip)
                .all()
            )

    def get_by_document_ids(self, db: Session, *, document_ids: list) -> List[Clue]:
        return db.query(self.model).filter(self.model.rule_id in document_ids)

    def get_multi_clue(
        self, db: Session, *, query: ClueQuery, skip: int = 0, limit: int = 100
    ) -> List[Clue]:
        filter_conditions = [
            or_(
                self.model.remarks.ilike(f"%{query.keywords}%"),
                self.model.clue_detail.ilike(f"%{query.keywords}%"),
                self.model.mention_elements.ilike(f"%{query.keywords}%"),
            ),
            or_(
                self.model.status == int(query.status),
                and_(int(query.status) == 4, self.model.status != 0),
                int(query.status) == -1,
            ),
            or_(self.model.clue_type == query.clue_type, query.clue_type is None),
            or_(
                self.model.is_favorite == int(query.is_favorite),
                int(query.is_favorite) == -1,
            ),
            or_(self.model.topic == query.topic, query.topic is None),
            or_(self.model.rule_id.in_(query.rule_id_list), query.rule_id_list is None),
            getattr(self.model, query.time_span_item, "create_time").between(
                query.start_time, query.end_time
            ),
        ]

        # 根据给定的排序选项进行排序，默认按照线索推荐时间进行排序
        if query.sort == "desc":
            order_by = getattr(self.model, query.sort_item, "create_time").desc()
        else:
            order_by = getattr(self.model, query.sort_item, "create_time").asc()

        if limit == -1:
            return (
                db.query(self.model)
                .filter(and_(*filter_conditions))
                .order_by(order_by)
                .offset(skip)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .filter(and_(*filter_conditions))
                .order_by(order_by)
                .limit(limit)
                .offset(skip)
                .all()
            )

    def update_clue(self, db: Session, *, db_obj: Clue, obj_in: ClueUpdate) -> Clue:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                if field == "status" or field == "is_favorite":
                    print(field)
                    setattr(db_obj, field, int(update_data[field]))
                else:
                    setattr(db_obj, field, update_data[field])
        if "update_time" in obj_data:
            setattr(db_obj, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def judge_clue_list(self, db: Session, *, clue_id_list, status):
        db.query(self.model).filter(self.model.clue_id.in_(clue_id_list)).update(
            {
                self.model.status: int(status),
                self.model.update_time: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        db.commit()

    def delete_by_clue_id(self, db: Session, *, clue_id: str) -> Clue:
        obj = self.get_by_clue_id(db=db, clue_id=clue_id)
        db.delete(obj)
        db.commit()
        return obj

    def delete_by_clue_list(self, db: Session, *, delete_list: List[Clue]):
        for clue in delete_list:
            db.delete(clue)
        db.commit()


clue = CRUDClue(Clue)
