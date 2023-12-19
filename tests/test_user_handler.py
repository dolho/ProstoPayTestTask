import uuid

import pytest
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from source.user_handler.models import User
from source.user_handler.pydantic_models import UserReadDTO
from source.user_handler.user_handler import UserHandler
from tests.factories.user import pydantinc_user_factory, user_factory


@pytest.fixture
def user_handler(async_db_session: AsyncSession) -> UserHandler:
    return UserHandler(async_db_session)


@pytest.mark.asyncio
async def test_retrieve_user_handler(
    user_handler: UserHandler,
    async_db_session: AsyncSession,
) -> None:
    first_name, last_name, password = (
        "TestUserName",
        "example@example.com",
        "strongPassword",
    )
    user_id = await user_factory(async_db_session, first_name, last_name, password)
    await user_factory(async_db_session, first_name, last_name, password)

    user = await user_handler.get(user_id)
    assert user is not None
    assert isinstance(user, UserReadDTO)
    assert user.id == user_id
    assert user.first_name == first_name
    assert user.last_name == last_name


@pytest.mark.asyncio
async def test_retrieve_non_existing_user(
    user_handler: UserHandler,
    async_db_session: AsyncSession,
) -> None:
    user_id = uuid.uuid4()
    user = await user_handler.get(user_id)
    assert user is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "first_name, last_name, password",
    [
        ("TestUserName", "example@example.com", "strongPassword"),
        ("TestUserName", "example@example.com", "weakPassword"),
    ],
)
async def test_post_user_handler(
    async_db_session: AsyncSession,
    user_handler: UserHandler,
    first_name: str,
    last_name: str,
    password: str,
) -> None:
    user_write = await pydantinc_user_factory(first_name, last_name, password)

    await user_handler.post(user_write)

    user = await async_db_session.get(User, user_write.id)
    assert user is not None
    assert user.first_name == user_write.first_name
    assert user.last_name == user_write.last_name


@pytest.mark.asyncio
async def test_post_user_handler_fails_on_invalid_type(
    async_db_session: AsyncSession,
    user_handler: UserHandler,
) -> None:
    first_name, last_name, password = (
        "TestUserName",
        "example@example.com",
        "strongPassword",
    )
    user_write = await pydantinc_user_factory(first_name, last_name, password)

    with pytest.raises(AttributeError):
        await user_handler.post(user_write.model_dump())  # type: ignore


@pytest.mark.asyncio
async def test_post_user_handler_fails_repetative_insert(
    async_db_session: AsyncSession,
    user_handler: UserHandler,
) -> None:
    first_name, last_name, password = (
        "TestUserName",
        "example@example.com",
        "strongPassword",
    )
    user_write = await pydantinc_user_factory(first_name, last_name, password)

    await user_handler.post(user_write)

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await user_handler.post(user_write)
