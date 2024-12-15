from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from .utils import random_lower_string, random_email
import time
import json


# 测试创建用户
# POST /api/v1/users/
def test_create_user_new_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user_name = "test"
    password = random_lower_string()
    old_user = crud.user.get_by_user_name(db, user_name=user_name)
    if old_user:
        crud.user.delete_by_user_id(db, user_id=old_user.user_id)
    data = {"user_name": user_name, "password": password}
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    assert user_name == created_user["user_name"]
    # crud.user.delete_by_user_id(db, user_id=new_user.user_id)


# 测试根据id查询用户
# GET /api/v1/users/
def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user_name = "test"
    user = crud.user.get_by_user_name(db, user_name=user_name)
    if user:
        user_id = user.user_id
        r = client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.user.get_by_user_name(db, user_name=user_name)
        assert user
        assert user.user_name == created_user["user_name"]
        # user = crud.user.delete_by_user_id(db, user_id=user.user_id)


# 测试超级用户当前状态
# GET /api/v1/users/me
def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: dict
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == 1
    assert current_user["is_admin"] == 1
    assert current_user["user_name"] == settings.FIRST_SUPERUSER


# 测试普通用户当前状态
# GET /api/v1/users/me
def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: dict
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    assert 200 <= r.status_code < 300
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == 1
    assert current_user["is_admin"] == 0
    assert current_user["user_name"] == settings.TEST_USER


# 测试普通用户更新
# PUT /api/v1/users/me
def test_update_user_me(client: TestClient, normal_user_token_headers: dict) -> None:
    email = random_email()
    data = {"email": email}
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.put(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers, json=data
    )
    assert 200 <= r.status_code < 300
    current_user = r.json()
    assert current_user
    assert current_user["email"] == email


# 测试获取用户列表
# GET /api/v1/users/responsible_user
def test_read_responsible_user(
    client: TestClient, normal_user_token_headers: dict
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/responsible_user",
        headers=normal_user_token_headers,
    )
    user_list = r.json()
    assert 200 <= r.status_code < 300
    assert len(user_list) >= 1
    for user in user_list:
        assert "user_name" in user


# 公开注册用户
# POST /api/v1/users/open
def test_create_user_open(client: TestClient, db: Session) -> None:
    email = random_email()
    user_name = "test"
    password = random_lower_string()
    old_user = crud.user.get_by_user_name(db, user_name=user_name)
    if old_user:
        crud.user.delete_by_user_id(db, user_id=old_user.user_id)
    data = {"user_name": user_name, "email": email, "password": password}
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.post(f"{settings.API_V1_STR}/users/open", json=data)
    assert 200 <= r.status_code < 300
    current_user = r.json()
    assert current_user
    assert current_user["email"] == email
    assert current_user["user_name"] == user_name


# 测试根据user_id获取用户信息，限定超级用户
# GET /api/v1/users/{user_id}
def test_read_user_by_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    user_name = "test"
    password = random_lower_string()
    old_user = crud.user.get_by_user_name(db, user_name=user_name)
    if old_user:
        user_id = old_user.user_id
    else:
        data = {"user_name": user_name, "email": email, "password": password}
        r = client.post(f"{settings.API_V1_STR}/users/open", json=data)
        old_user = r.json()
        user_id = old_user["user_id"]
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    current_user = r.json()
    # print(current_user)
    assert current_user
    assert current_user["user_id"] == user_id


# 测试根据user_id更新用户信息，限定超级用户
# POST /api/v1/users/{user_id}
def test_update_user_by_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    user_name = "test"
    password = random_lower_string()
    old_user = crud.user.get_by_user_name(db, user_name=user_name)
    if old_user:
        user_id = old_user.user_id
    else:
        data = {"user_name": user_name, "email": email, "password": password}
        r = client.post(f"{settings.API_V1_STR}/users/open", json=data)
        old_user = r.json()
        user_id = old_user["user_id"]
    email = random_email()
    data = {
        "user_name": user_name,
        "nick_name": "test_nick",
        "email": email,
        "phone": "123456",
        "description": "test",
        "is_admin": 0,
        "is_active": 1,
        "password": "123456",
    }
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.put(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    current_user = r.json()
    # print(current_user)
    assert current_user
    assert current_user["email"] == data["email"]
    assert current_user["nick_name"] == data["nick_name"]
