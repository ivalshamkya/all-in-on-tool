from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class Example(BaseModel):
    id: str = Field(alias="_id")
    name: Optional[str] = None
