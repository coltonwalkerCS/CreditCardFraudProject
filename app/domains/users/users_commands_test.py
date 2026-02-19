# tests/domains/users/test_user_commands.py
from __future__ import annotations

import uuid

import pytest

from app.domains.users.dtos import UserCreateRequestDto, UserUpdateRequestDto
from app.domains.users.users_commands import (
    UsernameAlreadyExistsError,
    UserNotFoundError,
    create_user,
    delete_user,
    get_user_by_id,
    update_user,
)


def test_create_user_success(session):
    created = create_user(session, UserCreateRequestDto(username="colton"))

    assert created.username == "colton"
    assert created.id is not None
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_user_duplicate_username_raises(make_user, session):
    make_user("dup")
    with pytest.raises(UsernameAlreadyExistsError):
        create_user(session, UserCreateRequestDto(username="dup"))


def test_get_user_by_id_not_found(session):
    with pytest.raises(UserNotFoundError):
        get_user_by_id(session, uuid.uuid4())


def test_update_user_success(make_user, session):
    created = make_user("oldname")
    updated = update_user(session, created.id, UserUpdateRequestDto(username="newname"))

    assert updated.id == created.id
    assert updated.username == "newname"


def test_update_user_duplicate_username_raises(make_user, session):
    u1 = make_user("user1")
    make_user("user2")

    with pytest.raises(UsernameAlreadyExistsError):
        update_user(session, u1.id, UserUpdateRequestDto(username="user2"))


def test_delete_user_success(make_user, session):
    created = make_user("todelete")

    delete_user(session, created.id)

    with pytest.raises(UserNotFoundError):
        get_user_by_id(session, created.id)
