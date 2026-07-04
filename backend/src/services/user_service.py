from starlette import status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

import uuid
from datetime import timedelta, datetime, timezone

import bcrypt
from jose import JWTError, jwt

from ..config import SECRET_KEY, ALGORITHM

# needed models
from ..models import User

# needed repos
from ..repository.user_repository import UserRepository


def verify_password(plain_pwd:str, hashed_pwd:str):
    return bcrypt.checkpw(plain_pwd.encode('utf-8'), hashed_pwd.encode('utf-8'))


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


class UserService:

    def __init__(self, db):
        self.db = db
        self.repo = UserRepository(db)
    

    async def create_refresh_token(self, user: User, expires_delta: timedelta):
        expira = datetime.now(timezone.utc) + expires_delta
        payload = {"user_id": str(user.id), "email": user.email, "exp": expira, "type": "refresh"}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


    async def refresh(self, refresh_token):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token ausente")

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido para essa operação")

        user = self.repo.get_user_by_id(user_id=payload["user_id"])
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        new_access_token = await self.create_access_token(user, timedelta(minutes=20))

        return {"access_token": new_access_token, "token_type": "bearer"}

    async def create_access_token(self, user: User, expires_delta:timedelta):
        expires = datetime.now(timezone.utc) + expires_delta
        encoded_access_token = jwt.encode(
            {"user_id": str(user.id), "email": user.email, "role": user.role, "exp": expires, "type": "access"},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_access_token


    async def authenticate_user(self, email:str, password:str):
        user = self.repo.get_user_by_email(email)
        if not user: return False
        if not verify_password(password, user.hashed_password): return False
        return user

    async def create_user(
        self, username: str,
        email: str,
        hashed_password: str,
        role: str
    ) -> User:
        
        if self.repo.get_user_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já em uso.")
        
        return self.repo.create_user(str(uuid.uuid4()), username, email, hashed_password, role)