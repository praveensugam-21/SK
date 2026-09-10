from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginResponse, UserResponse
from app.utils.security import verify_password, create_access_token, create_refresh_token
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginPayload(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user and return JWT token in httpOnly cookie and JSON response.
    Supports both JSON payload ({ email, password } or { username, password })
    and Form-encoded payload (application/x-www-form-urlencoded / multipart).
    """
    email = None
    password = None

    # Try parsing JSON first
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            email = body.get("email") or body.get("username")
            password = body.get("password")
        except Exception:
            pass

    # If not JSON, try form data
    if not email or not password:
        try:
            form = await request.form()
            email = form.get("username") or form.get("email")
            password = form.get("password")
        except Exception:
            pass

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email and password are required",
        )

    email = str(email).strip().lower()

    result = await db.execute(
        select(User).filter(User.email.ilike(email), User.deleted_at.is_(None))
    )
    user = result.scalars().first()

    if not user or not verify_password(str(password), user.password_hash):
        if user:
            user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Check lockout
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is temporarily locked. Try again later.",
        )

    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh = create_refresh_token(data={"sub": str(user.id)})

    # Set auth cookies
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=1800,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        samesite="lax",
        max_age=604800,
        path="/",
    )

    return LoginResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/logout")
async def logout(response: Response):
    """Clear auth cookies."""
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return UserResponse.model_validate(current_user)


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token."""
    from app.utils.security import decode_token
    from jose import JWTError

    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    result = await db.execute(
        select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    )
    user = result.scalars().first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    new_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    response.set_cookie(
        key="access_token",
        value=new_token,
        httponly=True,
        samesite="lax",
        max_age=1800,
        path="/",
    )
    return {"access_token": new_token, "token_type": "bearer"}
