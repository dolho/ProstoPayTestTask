from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseUserDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class UserReadDTO(BaseUserDTO):
    """A class for accessing user data."""

    model_config = ConfigDict(from_attributes=True)


class UserWriteDTO(BaseUserDTO):
    """A class for writing user data."""

    # An example of a field, that should be allowed to read only in specific cases
    # due to sensitivity of the data stored in it
    password: str
