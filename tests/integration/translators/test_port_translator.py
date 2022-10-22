from models import Port
from structure import port_translator


class TestPortTranslator:
    def setup(self):
        self.translator = port_translator

    def test_from_json(self):
        port_id = "22"
        status = "open"
        service = "ssh"
        protocol = "tcp"
        json = {
            "@protocol": protocol,
            "@portid": port_id,
            "state": {
                "@state": status,
                "@reason": "syn-ack",
                "@reason_ttl": "0"
            },
            "service": {
                "@name": service,
                "@method": "table",
                "@conf": "3"
            }
        }
        result = self.translator.from_json(json)
        assert isinstance(result, Port)
        assert result.port_id == port_id
        assert result.status == status
        assert result.service == service
        assert result.protocol == protocol
