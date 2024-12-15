from sqlalchemy import BigInteger, Integer, VARCHAR, DateTime, Column
from app.db.base_class import Base


class Task(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    task_id = Column(VARCHAR(11), nullable=False)
    task_name = Column(VARCHAR(255), nullable=False)
    source = Column(VARCHAR(255), nullable=False)
    type = Column(VARCHAR(11), nullable=False)
    status = Column(Integer, nullable=False)
    description = Column(VARCHAR(500))
    owner_user_id = Column(VARCHAR(11), nullable=False)
    responsible_user_id = Column(VARCHAR(11))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    create_time = Column(DateTime, nullable=False)
