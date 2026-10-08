from datetime import datetime, UTC, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from config import settings

from typing import Annotated
from fastapi import Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from database import get_db

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str) -> str | None:
    """Verify a JWT access token and return the user_id if valid."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> models.User:
    """Get the current user from the JWT access token."""
    user_id = verify_access_token(token)
    if user_id is None:
        raise unauthorized_exception("Invalid or expired token")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        raise unauthorized_exception("Invalid or expired token")
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id_int))
    user = result.scalar_one_or_none()
    if not user:
        raise unauthorized_exception("User not found")
    return user


def unauthorized_exception(detail: str) -> HTTPException:
    """Return an HTTPException for invalid or expired tokens."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


CurrentUser = Annotated[models.User, Depends(get_current_user)]
