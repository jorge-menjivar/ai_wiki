from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = ''
    leaky_bucket_token_limit: int = 20
    leaky_bucket_time_window: int = 60*60
    host: str = ''
    mystic_api_token: str = ''
    mystic_gpt3_neo_2_7b_id: str = ''
    mystic_gpt3_j_id: str = ''
    openai_api_key: str = ''
    postgres_host: str = ''
    postgres_db: str = ''
    postgres_user: str = ''
    postgres_pass: str = ''
    url: str = ''

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
