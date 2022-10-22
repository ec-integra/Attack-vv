from models import Port


class PortTranslator:
    def from_json(self, json) -> Port:
        model = Port()
        model.port_id = json.get("@portid")
        model.status = json.get("state", {}).get("@state")
        model.service = json.get("service", {}).get("@name")
        model.protocol = json.get("@protocol")
        return model
