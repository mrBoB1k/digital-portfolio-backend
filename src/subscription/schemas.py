from pydantic import BaseModel

class Sub(BaseModel):
    id: int
    first_name: str
    last_name: str

class Mas(BaseModel):
    message: str