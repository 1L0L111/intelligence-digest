from typing import Protocol, TypeVar, Type
from pydantic import BaseModel
T = TypeVar("T", bound=BaseModel)
class LLMProvider(Protocol):
    async def structured(self, system: str, user: str, schema: Type[T]) -> T: ...
