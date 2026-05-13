# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token, RefreshRequest
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token

from fastapi import Body
from app.core.security import verify_token
from app.services.auth_service import get_user_by_email

from fastapi.security import OAuth2PasswordRequestForm


from fastapi import Request
from app.core.limiter import limiter

# Authentication routes
router = APIRouter(prefix="/auth", tags=["Authentication"])

# User registration endpoint
@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
def register(  request: Request,user: UserCreate, db: Session = Depends(get_db)):

    new_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
        
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    return new_user

# User login endpoint
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )




from app.core.security import verify_token, create_access_token
from app.schemas.auth import Token

@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
def refresh_token(
    request: Request,
    request_data: RefreshRequest
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(
        token=request_data.refresh_token,
        credentials_exception=credentials_exception,
        token_type="refresh"
    )

    new_access_token = create_access_token(
        data={"sub": token_data["email"]}
    )

    return Token(
        access_token=new_access_token,
        refresh_token=request_data.refresh_token,
        token_type="bearer"
    )



from app.core.deps import get_current_user, require_role


@router.get("/admin/dashboard")
def admin_dashboard(
    user = Depends(require_role("admin"))
):
    return {"message": "Welcome Admin"}

@router.get("/profile", response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return user