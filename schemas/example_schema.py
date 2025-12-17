from pydantic import BaseModel
from uuid import UUID

class Example(BaseModel):
    id: UUID
    description: str
