from sqlalchemy import BigInteger, VARCHAR, DateTime, Column, JSON, Integer
from app.db.base_class import Base


class Clue(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    clue_id = Column(VARCHAR(11), nullable=False)
    rule_id = Column(VARCHAR(11), nullable=False)
    clue_type = Column(VARCHAR(10), nullable=False)
    document_id = Column(VARCHAR(255), nullable=False)
    status = Column(Integer, nullable=False, default=0)
    clue_detail = Column(JSON, nullable=False)
    mention_elements = Column(JSON, nullable=False)
    origin_create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    create_time = Column(DateTime, nullable=False)
    remarks = Column(VARCHAR(500))
    is_favorite = Column(Integer, nullable=False, default=0)
    topic = Column(VARCHAR(255), nullable=False)
