import pydantic
import typing as t

class ActionRequest(pydantic.BaseModel):
    action: t.Literal["forward", "backward", "left", "right", "stop"]