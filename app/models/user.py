from sqlalchemy import BigInteger, Integer, VARCHAR, DateTime, Column
from app.db.base_class import Base


class User(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(VARCHAR(11), nullable=False)
    user_name = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    nick_name = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    phone = Column(VARCHAR(255))
    is_admin = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)
    description = Column(VARCHAR(500))
    update_time = Column(DateTime, nullable=False)
    create_time = Column(DateTime, nullable=False)
    remarks = Column(VARCHAR(500))
