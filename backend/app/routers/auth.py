from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from .. import auth, db

router = APIRouter(prefix="/api/auth", tags=["auth"])


class Credentials(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(body: Credentials) -> dict:
    if len(body.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    existing = await db.fetchrow(
        "select id from users where email = $1", body.email.lower()
    )
    if existing:
        raise HTTPException(409, "An account with this email already exists")
    user_id = await db.fetchval(
        "insert into users(email, password_hash) values($1,$2) returning id",
        body.email.lower(), auth.hash_password(body.password),
    )
    return {"token": auth.create_token(str(user_id)), "email": body.email.lower()}


@router.post("/login")
async def login(body: Credentials) -> dict:
    row = await db.fetchrow(
        "select id, password_hash from users where email = $1", body.email.lower()
    )
    if row is None or not auth.verify_password(body.password, row["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    return {"token": auth.create_token(str(row["id"])), "email": body.email.lower()}


@router.get("/me")
async def me(user: dict = Depends(auth.current_user)) -> dict:
    return {"id": str(user["id"]), "email": user["email"]}
