from models import Host, Network


class NetworkService:
    def filter_out_network_with_ports(self, network: Network) -> Network:
        network.tcp_hosts = self.__filter_out_hosts_with_ports(network.tcp_hosts)
        network.udp_hosts = self.__filter_out_hosts_with_ports(network.udp_hosts)
        network.ip_hosts = self.__filter_out_hosts_with_ports(network.ip_hosts)
        return network

    def __filter_out_hosts_with_ports(self, hosts: list[Host]) -> list[Host]:
        result = [
            host
            for host
            in hosts
            if host.ports
        ]
        return result
