from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.users import repo
from app.domains.users.dtos import (
    UserCreateRequestDto,
    UserResponseDto,
    UserUpdateRequestDto,
)


class UserNotFoundError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


def create_user(session: Session, request: UserCreateRequestDto) -> UserResponseDto:
    existing = repo.get_by_username(session, request.username)
    if existing is not None:
        raise UsernameAlreadyExistsError(request.username)

    user = repo.users_repo.insert(session, username=request.username)

    session.commit()
    session.refresh(user)

    return UserResponseDto.model_validate(user)


def get_user_by_id(session: Session, user_id: UUID) -> UserResponseDto:
    user = repo.users_repo.get_by_id(session, user_id)
    if user is None:
        raise UserNotFoundError(str(user_id))

    return UserResponseDto.model_validate(user)


def update_user(
    session: Session, user_id: UUID, dto: UserUpdateRequestDto
) -> UserResponseDto:
    user = repo.users_repo.get_by_id(session, user_id)
    if user is None:
        raise UserNotFoundError(str(user_id))

    updates = dto.model_dump(exclude_unset=True, exclude_none=True)

    # uniqueness rule only if username is changing
    if "username" in updates:
        new_username = updates["username"]
        existing = repo.get_by_username(session, new_username)
        if existing is not None and existing.id != user_id:
            raise UsernameAlreadyExistsError(new_username)

    repo.users_repo.update(user, **updates)

    session.commit()
    session.refresh(user)

    return UserResponseDto.model_validate(user)


def delete_user(session: Session, user_id: UUID) -> None:
    user = repo.users_repo.get_by_id(session, user_id)
    if user is None:
        raise UserNotFoundError(str(user_id))

    repo.users_repo.delete(session, user)
    session.commit()
