from typing import Optional
from models import Target


class Attack:
    def __init__(self):
        self.target: Optional[Target] = None
        self.contex: Optional[str] = None
        self.result: Optional[str] = None
        self.status: Optional[bool] = None


Attacks = list[Attack]
