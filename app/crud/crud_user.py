from typing import Any, Dict, Optional, Union, List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils import generate_id


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_user_name(self, db: Session, *, user_name: str) -> Optional[User]:
        return db.query(User).filter(User.user_name == user_name).first()

    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.user_id == user_id).first()

    def get_multi_responsible(
        self, db: Session, *, skip=0, limit=100, is_admin
    ) -> List[Optional[User]]:
        if is_admin == 1:
            return (
                db.query(self.model)
                .filter(User.is_active == 1)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .filter(User.is_active == 1)
                .filter(User.is_admin == is_admin)
                .offset(skip)
                .limit(limit)
                .all()
            )

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj_in_data["password"] = get_password_hash(obj_in_data["password"])
        obj_in_data["user_id"] = generate_id()
        db_obj = self.model(**obj_in_data, create_time=now_time, update_time=now_time)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, user_name: str, password: str
    ) -> Optional[User]:
        user = self.get_by_user_name(db, user_name=user_name)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin

    def delete_by_user_id(self, db: Session, *, user_id: str) -> User:
        obj = db.query(self.model).filter(self.model.user_id == user_id).first()
        db.delete(obj)
        db.commit()
        return obj


user = CRUDUser(User)
