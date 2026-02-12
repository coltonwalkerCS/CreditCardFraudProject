from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
