"""User service for business logic."""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.auth.password import hash_password, verify_password


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        result = await self.db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def authenticate_user(self, login_data: UserLogin) -> Optional[User]:
        """Authenticate a user."""
        user = await self.get_user_by_email(login_data.email)
        if not user:
            return None
        
        if not verify_password(login_data.password, user.hashed_password):
            return None
        
        return user
    
    async def update_user(self, user: User, **kwargs) -> User:
        """Update user information."""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
