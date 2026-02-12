from __future__ import annotations

import uuid

import pytest
from app.domains.users.commands import (
    UsernameAlreadyExistsError,
    UserNotFoundError,
    create_user,
    delete_user,
    get_user_by_id,
    update_user,
)
from app.domains.users.dtos import UserCreateRequestDto, UserUpdateRequestDto


def test_create_user_success(session):
    dto = UserCreateRequestDto(username="colton")

    created = create_user(session, dto)

    assert created.username == "colton"
    assert created.id is not None
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_user_duplicate_username_raises(session):
    create_user(session, UserCreateRequestDto(username="dup"))

    with pytest.raises(UsernameAlreadyExistsError):
        create_user(session, UserCreateRequestDto(username="dup"))


def test_get_user_by_id_not_found(session):
    with pytest.raises(UserNotFoundError):
        get_user_by_id(session, uuid.uuid4())


def test_update_user_success(session):
    created = create_user(session, UserCreateRequestDto(username="oldname"))

    updated = update_user(session, created.id, UserUpdateRequestDto(username="newname"))

    assert updated.id == created.id
    assert updated.username == "newname"


def test_update_user_duplicate_username_raises(session):
    u1 = create_user(session, UserCreateRequestDto(username="user1"))
    _u2 = create_user(session, UserCreateRequestDto(username="user2"))

    with pytest.raises(UsernameAlreadyExistsError):
        update_user(session, u1.id, UserUpdateRequestDto(username="user2"))


def test_delete_user_success(session):
    created = create_user(session, UserCreateRequestDto(username="todelete"))

    delete_user(session, created.id)

    with pytest.raises(UserNotFoundError):
        get_user_by_id(session, created.id)
