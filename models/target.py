from typing import Optional


class Target:
    def __init__(self):
        self.ip_address: Optional[str] = None
        self.mac_address: Optional[str] = None
        self.port_id: Optional[str] = None
        self.status: Optional[str] = None  # Which status has new target?
        self.service: Optional[str] = None
        self.protocol: Optional[str] = None


Targets = list[Target]
