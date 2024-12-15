import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
from jose import jwt
import time
import random
import hashlib

from app.core.config import settings


def page_data_list(items: list, page_no: int, page_size: int):
    total_count = len(items)
    total_page = total_count // page_size
    if total_count % page_size != 0:
        total_page += 1
    start = (page_no - 1) * page_size
    end = page_no * page_size
    if end > total_count:
        end = total_count
    final_items = items[start:end]
    return total_page, total_count, final_items


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(decoded_token)
        return decoded_token["user_name"]
    except jwt.JWTError:
        return None


def generate_id():
    timestamp = str(int(time.time()))
    rand_num = str(random.randint(0, 999999)).zfill(6)
    str_to_hash = timestamp + rand_num
    md5 = hashlib.md5()
    md5.update(str_to_hash.encode("utf-8"))
    return md5.hexdigest()[8:18]
