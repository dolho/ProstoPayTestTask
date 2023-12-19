from sqlalchemy.orm import declarative_base

# In a real world application environment variables would be used
TEST_DATABASE_ASYNC_URL = "postgresql+asyncpg://postgres:postgres@db/postgres"  # for non-docker env "postgresql+asyncpg://postgres:postgres@localhost:5454/postgres"


Base = declarative_base()
