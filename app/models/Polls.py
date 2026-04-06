
from typing import List, Optional, Sequence
from uuid import UUID, uuid4
from datetime import datetime, timezone

from .Choice import Choice
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

class PollCreate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    options: List[str]
    expires_at: Optional[datetime] = None
    
    
    @field_validator('options')
    @classmethod
    def validate_options(cls, v: List[str]) -> List[str]:
        if len(v) < 2 or len(v) > 5:
            raise HTTPException(
                status_code=400,
                detail="A poll must contain between 2 and 5 choices"
            )
        return v
    
    def create_poll(self) -> "Poll":
        options = [
            Choice(description=desc,
                   label= index+1
                   )
            for index, desc in enumerate(self.options)
        ]
        print(options)
        if self.expires_at is not None and self.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400,
                                detail="A poll's expiration must be in the future"
                                )
        
        return Poll(title=self.title, options=options, expires_at=self.expires_at)
            

class Poll(PollCreate):
    uuid: UUID = Field(default_factory=uuid4)
    options: List[Choice]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    