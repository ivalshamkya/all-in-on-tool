from datetime import date
from typing import Optional

from pydantic import BaseModel


class Example(BaseModel):
    id: str
    name: Optional[str] = None
