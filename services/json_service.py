import json
from models import Attack


class JsonService:
    def __init__(self, attacks_translator):
        self.attacks_translator = attacks_translator

    def parse_in_dict(self, filename: str) -> dict:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    def write_in_file(self, filename: str,
                      tcp_attacks: list[Attack],
                      udp_attacks: list[Attack],
                      arp_attacks: list[Attack]
                      ) -> None:
        with open(filename, 'w') as json_file:
            presented = {
                "tcp_attacks": self.attacks_translator.to_dict(tcp_attacks),
                "udp_attacks": self.attacks_translator.to_dict(udp_attacks),
                "arp_attacks": self.attacks_translator.to_dict(arp_attacks)
            }

            json.dump(presented, json_file, indent=2)
