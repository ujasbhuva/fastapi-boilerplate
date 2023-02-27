from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


# model for tag assign function end point
class GPTInput(BaseModel):
    text: constr(strip_whitespace=True, min_length=10, max_length=190, strict=True)


# model for tag assign function end point
class GenerationOutputDB(BaseModel):
    id: Optional[str]
    input: str
    raw_completion: str
    service: str
    tokens: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class GPtOutputDBUpdate(BaseModel):
    id: int
    input: Optional[str]
    raw_completion: Optional[str]
    service: Optional[str]
    tokens: Optional[int]
    rich_output: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class GenerationQuickUpdate(BaseModel):
    id: int
    raw_completion: Optional[str]
    tokens: Optional[int]


class BrowserToken(BaseModel):
    token: str


class GenerationId(BaseModel):
    id: int
