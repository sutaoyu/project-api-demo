from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
from app import crud
from app.core.config import settings


def get_task_info(db: Session):
    owner_user_name = "test"
    task_name = "测试任务"
    owner_user = crud.user.get_by_user_name(db, user_name=owner_user_name)
    owner_user_id = owner_user.user_id
    # 这里不加db.commit(),会因为mysql事务隔离导致无法读取新插入的数据
    # 参考：https://www.cnblogs.com/wintest/p/12825371.html
    db.commit()
    owner_task = crud.task.get_by_task_name_and_user(
        db, task_name=task_name, owner_user_id=owner_user_id
    )
    return task_name, owner_user_id, owner_task


# 测试创建任务
# POST /api/v1/tasks/
def test_create_task(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    task_name, owner_user_id, owner_task = get_task_info(db)
    responsible_user_name = "test"
    responsible_user = crud.user.get_by_user_name(db, user_name=responsible_user_name)
    responsible_user_id = responsible_user.user_id

    data = {
        "task_name": task_name,
        "source": "测试创建",
        "type": "daily",
        "description": "测试创建任务",
        "responsible_user_id": responsible_user_id,
        "start_time": "2023-10-24T06:59:36.992Z",
        "end_time": "2023-10-28T06:59:36.992Z",
    }
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.post(
        f"{settings.API_V1_STR}/tasks/create",
        headers=normal_user_token_headers,
        json=data,
    )
    if owner_task:
        assert r.status_code == 400
    else:
        assert 200 <= r.status_code < 300
        created_task = r.json()["data"]
        assert created_task["responsible_user_id"] == responsible_user_id
        assert created_task["owner_user_id"] == owner_user_id
        assert created_task["task_name"] == task_name


# 测试查询任务
# POST /api/v1/tasks/query
def test_query_task_multi(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {
        "sort": "desc",
        "page_no": 1,
        "page_size": 10,
        "type": "daily",
        "status": -1,
    }
    print("\npost_data:\n", data)
    r = client.post(
        f"{settings.API_V1_STR}/tasks/query",
        headers=normal_user_token_headers,
        json=data,
    )
    result = r.json()
    # print(result)
    assert 200 <= r.status_code < 300
    task_list = result["data"]["data_list"]
    assert len(task_list) >= 1
    for task in task_list:
        assert "task_id" in task
        assert task["type"] == "daily"


# 测试根据task_id查询任务
# GET /api/v1/tasks/{task_id}
def test_read_task(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    task_name, owner_user_id, owner_task = get_task_info(db)
    task_id = owner_task.task_id
    print("\ntask_id:\n", task_id)
    r = client.get(
        f"{settings.API_V1_STR}/tasks/{task_id}", headers=normal_user_token_headers
    )
    assert 200 <= r.status_code < 300
    task_info = r.json()["data"]
    assert task_info
    assert task_info["task_id"] == task_id
    assert task_info["task_name"] == task_name
    assert task_info["owner_user_id"] == owner_user_id


# 测试根据task_id更新任务
# PUT /api/v1/tasks/{task_id}
def test_update_task(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    task_name, owner_user_id, owner_task = get_task_info(db)
    task_id = owner_task.task_id
    data = {
        "task_name": "测试任务",
        "source": "测试创建",
        "type": "daily",
        "description": "测试创建任务-test",
        "responsible_user_id": "string",
        "start_time": "2023-10-24T11:37:19.657Z",
        "end_time": "2023-11-24T11:37:19.657Z",
    }
    print("\ntask_id:", task_id)
    print("\npost_data:\n", json.dumps(data, ensure_ascii=False))
    r = client.put(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    task_info = r.json()["data"]
    assert task_info
    assert task_info["description"] == data["description"]


# 测试根据task_id删除任务
# DELETE /api/v1/tasks/{task_id}
def test_delete_task(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    task_name, owner_user_id, owner_task = get_task_info(db)
    task_id = owner_task.task_id
    print("\ntask_id:", task_id)
    r = client.delete(
        f"{settings.API_V1_STR}/tasks/{task_id}", headers=normal_user_token_headers
    )
    assert 200 <= r.status_code < 300
    task_info = r.json()["data"]
    assert task_info
