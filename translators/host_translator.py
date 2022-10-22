from models import Host


class HostTranslator:
    def __init__(self, ports_translator):
        self.ports_translator = ports_translator

    def from_json(self, json) -> Host:
        address = json.get("address")
        if isinstance(address, dict):
            return self.__translate_dict_address(address, json)
        if isinstance(address, list):
            return self.__translate_list_address(address, json)
        return Host()

    def __translate_list_address(self, address: list, json: dict) -> Host:
        model = Host()
        if len(address) != 2:
            return model
        model.ip_address = address[0]["@addr"]
        model.mac_address = address[1]["@addr"]

        return self.__translate_ports(model, json)

    def __translate_dict_address(self, address: dict, json: dict):
        model = Host()
        model.ip_address = address.get("@addr")

        return self.__translate_ports(model, json)

    def __translate_ports(self, model: Host, json: dict) -> Host:
        json_ports_collection = json.get("ports", {}).get("port", [])
        model.ports = self.ports_translator.from_json(json_ports_collection)
        return model
