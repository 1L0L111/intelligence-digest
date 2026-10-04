from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Type, TypeVar
from app.config import settings
T = TypeVar("T", bound=BaseModel)
class OpenAICompatibleProvider:
    def __init__(self):
        self.client = AsyncOpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    async def structured(self, system: str, user: str, schema: Type[T]) -> T:
        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            response_format={"type":"json_object"}, temperature=0.1,
        )
        return schema.model_validate_json(response.choices[0].message.content)
