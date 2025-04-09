from pydantic import SecretStr
from pydantic_settings import BaseSettings

from typing import Optional

class Parameters(BaseSettings):
    discord_token: SecretStr 
    openai_api_key: SecretStr 
    openai_base_url: str
    llm_name: str
    fal_api_key: Optional[SecretStr] = None
    fal_model_slug: Optional[str] = None
    image_generation_chance: Optional[float] = 0.5

    def is_all_fal_data_present(self):
        return all([
            self.fal_api_key is not None,
            self.fal_model_slug is not None
        ])

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'