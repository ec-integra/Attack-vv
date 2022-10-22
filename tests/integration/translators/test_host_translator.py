from models import Host, Port
from structure import host_translator


class TestHostTranslator:
    def setup(self):
        self.translator = host_translator

    def test_from_json_address_list(self):
        ip_address = "192.168.0.1"
        mac_address = "C0:C9:E3:81:16:04"
        port_id = "22"
        port_status = "open"
        port_service = "ssh"
        port_protocol = "tcp"

        json = self.__get_host_address_list_case_json(
            ip_address,
            mac_address,
            port_id,
            port_status,
            port_service,
            port_protocol,
        )
        result = self.translator.from_json(json)
        assert isinstance(result, Host)
        assert result.ip_address == ip_address
        assert result.mac_address == mac_address
        assert len(result.ports) == 1
        port = result.ports[0]
        self.__assert_equal_port(
            port, port_id,
            port_status, port_service,
            port_protocol,
        )

    def test_from_json_address_dict(self):
        ip_address = "192.168.0.1"
        port_id = "22"
        port_status = "open"
        port_service = "ssh"
        port_protocol = "tcp"

        json = self.__get_host_address_dict_case_json(
            ip_address,
            port_id,
            port_status,
            port_service,
            port_protocol,
        )

        result = self.translator.from_json(json)
        assert isinstance(result, Host)
        assert result.ip_address == ip_address
        assert result.mac_address is None
        assert len(result.ports) == 1
        port = result.ports[0]
        self.__assert_equal_port(
            port, port_id,
            port_status, port_service,
            port_protocol,
        )

    def __assert_equal_port(
            self,
            port,
            port_id,
            status,
            service,
            protocol,
    ) -> None:
        assert isinstance(port, Port)
        assert port.port_id == port_id
        assert port.status == status
        assert port.service == service
        assert port.protocol == protocol

    def __get_host_address_list_case_json(
            self,
            ip_address: str,
            mac_address: str,
            port_id: str,
            port_status: str,
            port_service: str,
            port_protocol: str,
    ) -> dict:
        return {
            "address": [

                {"@addr": ip_address},
                {"@addr": mac_address},
            ],
            "ports": {
                "port": [
                    {
                        "@protocol": port_protocol,
                        "@portid": port_id,
                        "state": {
                            "@state": port_status,
                            "@reason": "syn-ack",
                            "@reason_ttl": "0"
                        },
                        "service": {
                            "@name": port_service,
                            "@method": "table",
                            "@conf": "3"
                        }
                    },
                ]
            },
        }

    def __get_host_address_dict_case_json(
            self,
            ip_address: str,
            port_id: str,
            port_status: str,
            port_service: str,
            port_protocol: str,
    ) -> dict:
        return {
            "address": {"@addr": ip_address},

            "ports": {
                "port": [
                    {
                        "@protocol": port_protocol,
                        "@portid": port_id,
                        "state": {
                            "@state": port_status,
                            "@reason": "syn-ack",
                            "@reason_ttl": "0"
                        },
                        "service": {
                            "@name": port_service,
                            "@method": "table",
                            "@conf": "3"
                        }
                    },
                ]
            },
        }
