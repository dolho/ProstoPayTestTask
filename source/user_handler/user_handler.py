from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from source.user_handler.models import User
from source.user_handler.pydantic_models import UserReadDTO, UserWriteDTO


class UserHandler:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, user_id: UUID) -> UserReadDTO | None:
        user_db = await self._session.get(User, user_id)
        return UserReadDTO.model_validate(user_db) if user_db is not None else None

    async def post(self, user: UserWriteDTO) -> None:
        new_user_db = User(**user.model_dump())
        self._session.add(new_user_db)
        await self._session.commit()
