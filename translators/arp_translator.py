from models import ArpTableItem


class ArpTranslator:
    def to_dict(self, model: ArpTableItem) -> dict:
        return {
            "ip_address": model.ip_address,
            "mac_address": model.mac_address,
        }
