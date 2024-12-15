from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
from app import crud
from app.core.config import settings
from app import schemas
import datetime
import time


owner_user_id = None
test_task = None
test_rule = None
test_event = None


def test_create_clue(client: TestClient, normal_user_token_headers: dict, db: Session):
    rule_id = "123"
    response = client.post(
        f"{settings.API_V1_STR}/clues/create/{rule_id}",
        headers=normal_user_token_headers,
        json={
            "clue_type": "message",
            "document_id": "test_test",
            "clue_detail": {},
            "mention_elements": {},
            "remarks": "",
            "is_favorite": 0,
        },
    )
    db.commit()
    assert 200 <= response.status_code < 300
    created_clue = response.json()["data"]
    assert created_clue["clue_type"] == "message"
    assert created_clue["rule_id"] == rule_id
    assert created_clue["document_id"] == "test_test"
    crud.clue.delete_by_clue_id(db=db, clue_id=created_clue["clue_id"])


def test_read_clue(client: TestClient, normal_user_token_headers: dict, db: Session):
    rule_id = "123"
    test_clue = crud.clue.create_one_with_rule(
        db=db,
        obj_in=schemas.ClueCreate(
            clue_type="message",
            document_id="test_test",
            clue_detail={},
            mention_elements={},
            is_favorite=0,
        ),
        rule_id=rule_id,
        topic="topic_demo",
    )

    response = client.get(
        f"{settings.API_V1_STR}/clues/{test_clue.clue_id}",
        headers=normal_user_token_headers,
    )
    assert 200 <= response.status_code < 300
    created_clue = response.json()["data"]
    assert created_clue["clue_type"] == "message"
    assert created_clue["rule_id"] == rule_id
    crud.clue.delete_by_clue_id(db=db, clue_id=created_clue["clue_id"])


def test_delete_clue(client: TestClient, normal_user_token_headers: dict, db: Session):
    rule_id = "123"
    test_clue = crud.clue.create_one_with_rule(
        db=db,
        obj_in=schemas.ClueCreate(
            clue_type="message",
            document_id="test_test",
            clue_detail={},
            mention_elements={},
            is_favorite=0,
        ),
        rule_id=rule_id,
        topic="topic_demo",
    )
    test_clue_id = test_clue.clue_id

    response = client.delete(
        f"{settings.API_V1_STR}/clues/{test_clue.clue_id}",
        headers=normal_user_token_headers,
    )
    db.commit()
    assert 200 <= response.status_code < 300
    test_clue = crud.clue.get_by_clue_id(db=db, clue_id=test_clue_id)
    assert test_clue is None
