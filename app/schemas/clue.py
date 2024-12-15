from typing import Optional, Any, List, Union, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel, Json, validator
from enum import IntEnum, Enum
from app.schemas.base import QueryBase, MultiResponseModel, TopicType
from pydantic.generics import GenericModel


class ClueType(str, Enum):
    message = "message"
    user = "user"
    chat = "chat"


class ClueStatus(int, Enum):
    unexamined = 0
    sensitive = 1
    relevant = 2
    irrelevant = 3


class ClueStatusUpdate(str, Enum):
    unexamined = "0"
    sensitive = "1"
    relevant = "2"
    irrelevant = "3"


class ClueIsFavorite(int, Enum):
    favorite = 1
    not_favorite = 0


class ClueBase(BaseModel):
    clue_type: ClueType
    document_id: str
    clue_detail: dict
    mention_elements: dict
    remarks: Optional[str] = ""
    is_favorite: ClueIsFavorite


# Properties to receive on Rule creation
class ClueCreate(ClueBase):
    pass


# Properties to receive on Rule update
class ClueUpdate(ClueBase):
    clue_type: Optional[ClueType] = None
    document_id: Optional[str] = None
    clue_detail: Optional[dict] = None
    mention_elements: Optional[dict] = None
    remarks: Optional[str] = None
    status: Optional[ClueStatus] = None
    is_favorite: Optional[ClueIsFavorite] = None


class JudgeClueList(BaseModel):
    clue_id_list: Optional[List[str]] = []
    status: Optional[ClueStatus] = None


class ClueInDBBase(ClueBase):
    clue_id: str
    rule_id: str
    create_time: datetime
    update_time: datetime
    origin_create_time: datetime
    topic: TopicType
    status: Optional[ClueStatus] = 0
    is_favorite: Optional[ClueIsFavorite] = 0

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class ClueInDB(ClueInDBBase):
    id: int


# Properties to return to client
class Clue(ClueInDBBase):
    pass


class ClueStatusQuery(IntEnum):
    unexamined = 0
    sensitive = 1
    public = 2
    irrelevant = 3
    all = -1
    examined = 4


class ClueIsFavoriteQuery(IntEnum):
    favorite = 1
    not_favorite = 0
    all = -1


class ClueSortItemQuery(str, Enum):
    origin_create_time = "origin_create_time"
    create_time = "create_time"
    update_time = "update_time"


class ClueTimeSpanItemQuery(str, Enum):
    origin_create_time = "origin_create_time"
    create_time = "create_time"
    update_time = "update_time"


class ClueQueryBase(QueryBase):
    is_fold_by_content: Optional[bool] = False
    sort_item: Optional[ClueSortItemQuery] = "create_time"
    time_span_item: Optional[ClueTimeSpanItemQuery] = "create_time"


class ClueQuery(ClueQueryBase):
    status: Optional[ClueStatusQuery] = -1
    clue_type: Optional[ClueType] = None
    task_id_list: List[str]
    rule_id_list: Optional[List[str]] = None
    keywords: Optional[str] = ""
    is_favorite: Optional[ClueIsFavoriteQuery] = -1
    topic: Optional[TopicType] = None

    @validator("task_id_list")
    def check_value(cls, v):
        if len(v) < 1:
            raise ValueError("len of task_id_list smaller than 0")
        return v


class ClueDownloadType(str, Enum):
    csv = "csv"
    txt = "txt"


class ClueDownload(BaseModel):
    download_type: Optional[ClueDownloadType] = "csv"
    clue_id_list: List[str]


class ClueIdListQuery(QueryBase):
    sort_item: Optional[ClueSortItemQuery] = "create_time"
    time_span_item: Optional[ClueTimeSpanItemQuery] = "create_time"


T = TypeVar("T")


class ClueMultiResponseModel(GenericModel, Generic[T]):
    data_list: List[T]
    pages: int
    total: int
    task_count: Optional[dict] = None
