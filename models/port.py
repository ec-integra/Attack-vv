from typing import Optional


class Port:
    def __init__(self):
        self.port_id: Optional[str] = None
        self.status: Optional[str] = None
        self.service: Optional[str] = None
        self.protocol: Optional[str] = None


Ports = list[Port]
