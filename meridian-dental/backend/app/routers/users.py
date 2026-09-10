from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid
from app.database import get_db
from app.dependencies import require_role, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.security import get_password_hash

router = APIRouter(prefix='/api/users', tags=['Users'])

@router.get('', response_model=List[UserResponse])
@router.get('/', response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    query = select(User).where(User.clinic_id == current_user.clinic_id)
    return (await db.execute(query)).scalars().all()

@router.post('', response_model=UserResponse)
@router.post('/', response_model=UserResponse)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    user = User(
        id=uuid.uuid4(),
        email=data.email,
        password_hash=get_password_hash(data.password),
        full_name=data.full_name,
        role=data.role,
        clinic_id=current_user.clinic_id,
        phone=data.phone,
        specialization=data.specialization,
        license_number=data.license_number
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get('/dentists', response_model=List[UserResponse])
async def list_dentists(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(User).where(User.clinic_id == current_user.clinic_id, User.role == 'dentist', User.is_active == True)
    return (await db.execute(query)).scalars().all()

@router.get('/{id}', response_model=UserResponse)
async def get_user(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    query = select(User).where(User.id == id, User.clinic_id == current_user.clinic_id)
    user = (await db.execute(query)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
