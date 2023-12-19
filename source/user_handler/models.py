import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from source.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(
        String, nullable=False
    )  # in a production environment it would be a hash of some sort
