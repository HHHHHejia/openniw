"""Email+password auth with JWT bearer tokens."""
import datetime as dt
import uuid

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.hash import pbkdf2_sha256

from . import db
from .config import get_settings

bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return pbkdf2_sha256.verify(password, password_hash)
    except ValueError:
        return False


def create_token(user_id: str) -> str:
    settings = get_settings()
    now = dt.datetime.now(dt.timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + dt.timedelta(hours=settings.token_ttl_hours),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


async def current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    settings = get_settings()
    try:
        payload = jwt.decode(creds.credentials, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    row = await db.fetchrow(
        "select id, email, created_at from users where id = $1",
        uuid.UUID(payload["sub"]),
    )
    if row is None:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(row)


async def case_owned_by(case_id: str, user: dict) -> dict:
    """Fetch a case and assert it belongs to `user`, else 404."""
    row = await db.fetchrow(
        "select * from cases where id = $1 and user_id = $2",
        uuid.UUID(case_id),
        user["id"],
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return dict(row)
