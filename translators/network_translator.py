from typing import Literal
from models import Network


class NetworkTranslator:
    def __init__(self, hosts_translator):
        self.hosts_translator = hosts_translator

    def from_json(self, json: dict) -> Network:
        network = Network()
        network.tcp_hosts = self.__get_hosts(json, "tcp_ports")
        network.udp_hosts = self.__get_hosts(json, "udp_ports")
        network.ip_hosts = self.__get_hosts(json, "protocols")
        network.current_ip_address = self.__get_key(json, "ip")
        network.current_networks_interface = self.__get_key(json, "current_network_interface")
        return network

    def __get_hosts(self, json, key: Literal["tcp_ports", "udp_ports", "protocols"]):
        hosts_json = json.get(f"{key}", {})\
            .get("nmaprun", {})\
            .get("host", [])
        return self.hosts_translator.from_json(hosts_json)

    def __get_key(self, json, key: Literal["ip", "current_network_interface"]):
        return json.get(f"{key}", {})
