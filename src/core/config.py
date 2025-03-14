from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App config
    AUTH_SECRET: str
    ERROR_LOG_FILENAME: str

    # Data Base config
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Redis config
    REDIS_HOST: str | None
    REDIS_PORT: str | None

    # Test Data Base config
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    # Email Verifier config
    VERIFIER_API_CODE: str
    VERIFIER_URL: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_NAME}"
)
DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{settings.DB_USER_TEST}:{settings.DB_PASS_TEST}"
    f"@{settings.DB_HOST_TEST}:{settings.DB_PORT_TEST}/{settings.DB_NAME_TEST}"
)
