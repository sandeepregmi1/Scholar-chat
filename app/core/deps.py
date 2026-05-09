from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(
        token=token,
        credentials_exception=credentials_exception,
        token_type="access"
    )

    user = db.query(User).filter(User.email == payload["email"]).first()

    if not user:
        raise credentials_exception

    return user

def require_role(required_role: str):

    def role_checker(current_user: User = Depends(get_current_user)):

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return role_checker