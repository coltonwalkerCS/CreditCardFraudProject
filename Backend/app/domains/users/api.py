from __future__ import annotations

from uuid import UUID

from app.db.session import get_session
from app.domains.users import commands
from app.domains.users.dtos import (
    UserCreateRequestDto,
    UserResponseDto,
    UserUpdateRequestDto,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreateRequestDto,
    session: Session = Depends(get_session),
) -> UserResponseDto:
    try:
        return commands.create_user(session, body)
    except commands.UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}", response_model=UserResponseDto)
def get_user(
    user_id: UUID,
    session: Session = Depends(get_session),
) -> UserResponseDto:
    try:
        return commands.get_user_by_id(session, user_id)
    except commands.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponseDto)
def update_user(
    user_id: UUID,
    body: UserUpdateRequestDto,
    session: Session = Depends(get_session),
) -> UserResponseDto:
    try:
        return commands.update_user(session, user_id, body)
    except commands.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except commands.UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        commands.delete_user(session, user_id)
    except commands.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        commands.delete_user(session, user_id)
    except commands.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
