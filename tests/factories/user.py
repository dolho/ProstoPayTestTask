from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from source.user_handler.models import User
from source.user_handler.pydantic_models import UserWriteDTO


# in a real project py_factoryboy would be a more suitable option to create factories
async def user_factory(
    session: AsyncSession, first_name: str, last_name: str, password: str
) -> UUID:
    user_id = uuid4()
    new_user = User(
        id=user_id, first_name=first_name, last_name=last_name, password=password
    )
    session.add(new_user)
    await session.commit()
    return user_id


async def pydantinc_user_factory(
    first_name: str, last_name: str, password: str
) -> UserWriteDTO:
    user_id = uuid4()
    new_user = UserWriteDTO(
        id=user_id, first_name=first_name, last_name=last_name, password=password
    )
    return new_user
