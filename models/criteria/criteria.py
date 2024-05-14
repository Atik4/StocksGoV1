from pydantic import BaseModel, validator
from typing import List, Union, Any

class Criteria(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    def is_satisfied(self, df: Any) -> bool:
        """Method to be overridden in each criterion implementation."""
        raise NotImplementedError("Each criterion must implement is_satisfied method.")