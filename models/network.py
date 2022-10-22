from typing import Optional
from .host import Hosts


class Network:
    def __init__(self):
        self.udp_hosts: Optional[Hosts] = None
        self.tcp_hosts: Optional[Hosts] = None
        self.ip_hosts: Optional[Hosts] = None
        self.current_ip_address: Optional[str] = None  # Who it's owner?
        self.current_networks_interface: Optional[str] = None  # networkS?
