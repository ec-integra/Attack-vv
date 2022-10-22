from structure import network_translator
from models import (
    Network,
    Host,
    Port,
)


class TestNetworkTranslator:
    def setup(self):
        self.translator = network_translator

    def test_from_json(self):
        json = self.__get_expected_json()
        result = self.translator.from_json(json)
        assert isinstance(result, Network)
        assert isinstance(result.tcp_hosts, list)
        assert isinstance(result.udp_hosts, list)

        number_of_tcp_hosts = 2
        assert len(result.tcp_hosts) == number_of_tcp_hosts

        number_of_udp_hosts = 2
        assert len(result.udp_hosts) == number_of_udp_hosts

        tcp_host_with_ports = result.tcp_hosts[0]
        assert isinstance(tcp_host_with_ports, Host)
        assert tcp_host_with_ports.ip_address == "192.168.0.1"
        assert tcp_host_with_ports.mac_address == "C0:C9:E3:81:16:04"

        tcp_ports = tcp_host_with_ports.ports
        number_of_tcp_ports = 2
        assert len(tcp_ports) == number_of_tcp_ports
        assert isinstance(tcp_ports, list)

        tcp_port_1 = tcp_ports[0]
        self.assert_equal_port(tcp_port_1, "22", "open", "ssh", "tcp")

        tcp_port_2 = tcp_ports[1]
        self.assert_equal_port(tcp_port_2, "53", "open", "domain", "tcp")

        tcp_host_without_ports = result.tcp_hosts[1]
        assert isinstance(tcp_host_without_ports, Host)
        assert tcp_host_without_ports.ip_address == "192.168.0.102"
        assert tcp_host_without_ports.mac_address is None
        assert tcp_host_without_ports.ports == []

        udp_host_with_ports = result.udp_hosts[0]
        assert isinstance(udp_host_with_ports, Host)
        assert udp_host_with_ports.ip_address == "192.168.0.104"
        assert udp_host_with_ports.mac_address == "E8:D0:FC:C4:08:19"

        udp_ports = udp_host_with_ports.ports
        number_of_udp_ports = 2
        assert len(udp_ports) == number_of_udp_ports
        assert isinstance(udp_ports, list)

        udp_port_1 = udp_ports[0]
        self.assert_equal_port(
            udp_port_1, "631", "open|filtered", "ipp", "udp",
        )

        udp_port_2 = udp_ports[1]
        self.assert_equal_port(
            udp_port_2, "5353", "open|filtered", "zeroconf", "udp",
        )

        udp_host_without_ports = result.udp_hosts[1]
        assert isinstance(udp_host_without_ports, Host)
        assert udp_host_without_ports.ip_address == "192.168.0.102"
        assert udp_host_without_ports.mac_address is None
        assert udp_host_without_ports.ports == []

    def assert_equal_port(
            self,
            port: Port,
            port_id: str,
            status: str,
            service: str,
            protocol: str
    ) -> None:
        assert isinstance(port, Port)
        assert port.port_id == port_id
        assert port.status == status
        assert port.service == service
        assert port.protocol == protocol

    def __get_expected_json(self) -> dict:
        return {
            "tcp_ports": {
                "nmaprun": {
                    "host": [
                        {
                            "address": [
                                {
                                    "@addr": "192.168.0.1"
                                },
                                {
                                    "@addr": "C0:C9:E3:81:16:04"
                                }
                            ],
                            "ports": {
                                "port": [
                                    {
                                        "@protocol": "tcp",
                                        "@portid": "22",
                                        "state": {
                                            "@state": "open"
                                        },
                                        "service": {
                                            "@name": "ssh"
                                        }
                                    },
                                    {
                                        "@protocol": "tcp",
                                        "@portid": "53",
                                        "state": {
                                            "@state": "open"
                                        },
                                        "service": {
                                            "@name": "domain"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "address": {
                                "@addr": "192.168.0.102"
                            },
                            "ports": {}
                        }
                    ]
                }
            },
            "udp_ports": {
                "nmaprun": {
                    "host": [
                        {
                            "address": [
                                {
                                    "@addr": "192.168.0.104"
                                },
                                {
                                    "@addr": "E8:D0:FC:C4:08:19"
                                }
                            ],
                            "ports": {
                                "port": [
                                    {
                                        "@protocol": "udp",
                                        "@portid": "631",
                                        "state": {
                                            "@state": "open|filtered"
                                        },
                                        "service": {
                                            "@name": "ipp"
                                        }
                                    },
                                    {
                                        "@protocol": "udp",
                                        "@portid": "5353",
                                        "state": {
                                            "@state": "open|filtered"
                                        },
                                        "service": {
                                            "@name": "zeroconf"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "address": {
                                "@addr": "192.168.0.102"
                            },
                            "ports": {}
                        }
                    ]
                }
            }
        }
