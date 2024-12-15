from typing import Dict
import random
import string
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)


def authentication_token_from_user_name(
    *, client: TestClient, user_name: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given user_name).

    If the user doesn't exist it is created first.
    """
    # password = random_lower_string()
    password = settings.TEST_USER_PASSWORD
    user = crud.user.get_by_user_name(db, user_name=user_name)
    if not user:
        user_in_create = UserCreate(user_name=user_name, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(user_name=user_name, password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(
        client=client, username=user_name, password=password
    )


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    username = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    domains = ["example.com", "gmail.com", "yahoo.com", "hotmail.com"]
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    return email


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    print(tokens)
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
