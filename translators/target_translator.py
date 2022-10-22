from models import Target


class TargetTranslator:
    def to_dict(self, model: Target) -> dict:
        return {
            "ip_address": model.ip_address,
            "mac_address": model.mac_address,
            "port_id": model.port_id,
            "status": model.status,
            "service": model.service,
            "protocol": model.protocol
        }
