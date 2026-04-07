from uuid import UUID, uuid4

from pydantic import BaseModel,Field


class ChoiceCreate(BaseModel):
    
    description: str = Field(min_length=1, max_length=100)
    
class Choice(ChoiceCreate):
    
    id: UUID = Field(default_factory=uuid4)
    label: int = Field(ge=1, le=6)
    