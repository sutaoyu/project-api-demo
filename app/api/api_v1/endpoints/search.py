import math
import re
from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException, Body, Query
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Any
from app import schemas
from app.schemas.base import ResponseModel, MultiResponseModel
from app.core.config import settings
from app.api import deps
from app.utils import page_data_list


es = Elasticsearch(hosts=settings.ES_DATABASE_URI, timeout=50000)
router = APIRouter()


def simple_search_criteria(query: schemas.SimpleSearchQuery) -> Any:
    body = {"size": 100, "query": {"match": {"A_content": query.keywords}}}
    result_list = es.search(index=settings.index_crypted_message, body=body)
    return result_list


@router.post("/simple", response_model=ResponseModel[MultiResponseModel[dict]])
def simple_search(
    *,
    db: Session = Depends(deps.get_db),
    query: schemas.SimpleSearchQuery,
) -> Any:
    result = simple_search_criteria(query)
    total_page, total_count, final_items = page_data_list(
        result["hits"]["hits"], query.page_no, query.page_size
    )
    data = {"data_list": final_items, "pages": total_page, "total": total_count}
    return ResponseModel(code=200, msg="ok", data=data)
