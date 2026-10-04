from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    llm_base_url: str = "http://localhost:8001/v1"
    llm_api_key: str = "change-me"
    llm_model: str = "qwen3.6-35b-a3b"
    embedding_model: str = "intfloat/multilingual-e5-base"
    top_k: int = 30
    digest_size: int = 10
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
