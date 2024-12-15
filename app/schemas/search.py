from enum import Enum

from pydantic import BaseModel

from app.schemas import QueryBase
from typing import Optional


class SimpleSearchQuery(QueryBase):
    keywords: Optional[str] = ""
