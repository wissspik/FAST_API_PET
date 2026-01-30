from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import User
from backend.entrance.models.models import ProfileOut, ProfileUpdate
from backend.entrance.utils.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])


def _profile_out(user: User) -> ProfileOut:
    return ProfileOut(login=user.login, email=user.email, phone=user.phone)


@router.get("", response_model=ProfileOut)
async def get_profile(user: User = Depends(get_current_user)) -> ProfileOut:
    return _profile_out(user)


@router.patch("", response_model=ProfileOut)
async def update_profile(
    data: ProfileUpdate,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ProfileOut:
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    if "email" in data.model_fields_set:
        user.email = data.email
    if "phone" in data.model_fields_set:
        user.phone = data.phone

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or phone already used",
        )
    await session.refresh(user)
    return _profile_out(user)
