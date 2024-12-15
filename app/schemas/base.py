from pydantic.generics import GenericModel
from typing import Any, Generic, List, Optional, TypeVar, Dict
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from enum import Enum, IntEnum

T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    code: int
    data: T
    msg: str


class MultiResponseModel(GenericModel, Generic[T]):
    data_list: List[T]
    pages: int
    total: int


class QueryBase(BaseModel):
    sort: str = "desc"
    page_no: int = 1
    page_size: int = 10
    start_time: datetime = "2000-01-01 00:00:00"
    end_time: datetime = "2099-01-01 00:00:00"

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}

    @validator("page_no", "page_size")
    def check_value(cls, v):
        if v < 1:
            raise ValueError("value of page_no or page_size smaller than 0")
        return v

    @validator("sort")
    def check_sort(cls, v):
        if v not in ["desc", "asc"]:
            raise ValueError('sort can only be "desc" or "asc"')
        return v


class TopicType(str, Enum):
    sale_agent = "topic_demo"
