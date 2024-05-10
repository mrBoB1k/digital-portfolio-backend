from typing import List, Optional, Union

from pydantic import BaseModel

class UserList(BaseModel):
    id: int
    first_name: str
    last_name: str
    city:str
    technology: Optional[Union[List[str], None]]  # сделано поле опциональным и может быть списком строк или None


class TechnologyList(BaseModel):
    technology: Optional[Union[List[str], None]]