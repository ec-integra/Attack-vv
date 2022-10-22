import json
from models import Attack


class AttackJsonRepository:
    def __init__(self, attacks_translator):
        self.attacks_translator = attacks_translator

    def write_in_file(self, filename: str,
                      tcp_attacks: list[Attack],
                      udp_attacks: list[Attack],
                      arp_attacks: list[Attack],
                      brute_force_attacks: list[Attack],
                      dhcp_stavation_attack: list[Attack]
                      ) -> None:
        with open(filename, 'w') as json_file:
            presented = {
                "tcp_attacks": self.attacks_translator.to_dict(tcp_attacks),
                "udp_attacks": self.attacks_translator.to_dict(udp_attacks),
                "arp_attacks": self.attacks_translator.to_dict(arp_attacks),
                "brute_force_attacks": self.attacks_translator.to_dict(brute_force_attacks),
                "dhcp_stavation_attack": self.attacks_translator.to_dict(dhcp_stavation_attack)
            }

            json.dump(presented, json_file, indent=2)
