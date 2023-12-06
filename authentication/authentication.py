from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.models import User, AccessToken
from database.database import get_database_session
from authentication.password import verify_password, generate_token


def authenticate(email: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(user: User, db: Session) -> AccessToken:
    access_token = db.query(AccessToken).join(
        User).filter(AccessToken.user_id == user.id).first()
    if access_token is not None:
        if datetime.now() > access_token.expiration_date:
            db.delete(access_token)
            db.commit()
        else:
            return access_token
    tomorrow = datetime.now() + timedelta(days=1)
    accessToken = AccessToken(
        user_id=user.id, expiration_date=tomorrow, access_token=generate_token())
    db.add(accessToken)
    db.commit()
    db.refresh(accessToken)
    return accessToken


# api_key_token = APIKeyHeader(name='Token')


# def verify_access_token(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
auth_schema = OAuth2PasswordBearer(tokenUrl='/token')


def verify_access_token(token: str = Depends(auth_schema), db: Session = Depends(get_database_session)):
    gettoken = db.query(AccessToken).first()
    print(gettoken.access_token)
    get_token = db.query(AccessToken).join(User).filter(
        AccessToken.access_token == token).first()
    print('accesstoken', get_token)
    if gettoken is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if datetime.now() > gettoken.expiration_date:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return gettoken.user


api_key_token = APIKeyHeader(name='Token')


def logout(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).join(User).filter(
        AccessToken.access_token == token).first()
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db.delete(access_token)
    db.commit()
