from typing import Literal, Optional
from models import Attack, Target
from attacks import DhcpStarvationAttack

class AttackService:
    def __init__(
            self,
            shell_command_translator,
            invoker_shell_command_service,
            target_service,
            result_attack_service,
            multiprocessing_attack_wrapper
    ):
        self.shell_command_translator = shell_command_translator
        self.invoker_shell_command_service = invoker_shell_command_service
        self.target_service = target_service
        self.result_attack_service = result_attack_service
        self.multiprocessing_attack_wrapper = multiprocessing_attack_wrapper

    def create_dhcp_starvation_attack(self, network_interface) -> list[Attack]:
        result_attack = []
        dhcp_starvation_attack = DhcpStarvationAttack(network_interface)
        attack = Attack()
        target = self.target_service.create_target(ip_address=None,mac_address=None,port_id=None,status=None,
                                                   service=None, protocol = "dhcp")
        status_attack = dhcp_starvation_attack.get_status_attack()
        attack.target = target
        attack.status = status_attack

        result_attack.append(attack)
        return result_attack

    def create_attack(
            self,
            ip_address: str,
            mac_address: str,
            port_id: str,
            status_port: str,
            service: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood", "arp_spoofing", "brute_force"],
            ip_gateway: Optional[str] = None,
    ) -> Attack:
        type_to_func_mapping = {
            "syn_flood": self.__create_attacks_with_shell_commands,
            "udp_flood": self.__create_attacks_with_shell_commands,
            "arp_spoofing": self.__create_arp_spoofing_attack,
            "brute_force": self.__create_attacks_with_shell_commands
        }
        return type_to_func_mapping[type_attack](ip_address, mac_address, port_id, status_port,
                                                 service, protocol, type_attack, ip_gateway)

    def create_attacks(
            self,
            targets: list[Target],
            type_attack: Literal["syn_flood", "udp_flood", "arp_spoofing"],
            ip_gateway: Optional[str] = None,
    ) -> list[Attack]:
        result = []
        for item in targets:
            attack = self.create_attack(
                item.ip_address,
                item.mac_address,
                item.port_id,
                item.status,
                item.service,
                item.protocol,
                type_attack,
                ip_gateway
            )
            result.append(attack)
        return result

    def __create_attacks_with_shell_commands(
            self,
            ip_address: str,
            mac_address: str,
            port_id: str,
            status_port: str,
            service: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood", "arp_spoofing", "brute_force"],
            ip_gateway: Optional[str] = None,
    ) -> Attack:
        attack = Attack()
        target = self.target_service.create_target(ip_address, mac_address, port_id, status_port, service, protocol)
        contex = self.shell_command_translator.to_shell_command_attack(ip_address, port_id, service, type_attack)
        result = self.invoker_shell_command_service.invoke_one_command(contex)
        status_attack = self.result_attack_service.check_status_attack(type_attack, result)
        attack.target = target
        attack.contex = contex
        attack.result = result
        attack.status = status_attack
        return attack

    def __create_arp_spoofing_attack(
            self,
            ip_address: str,
            mac_address: str,
            port_id: str,
            status_port: str,
            service: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood", "arp_spoofing", "brute_force"],
            ip_gateway: Optional[str] = None,
    ) -> Attack:
        attack = Attack()
        target = self.target_service.create_target(
            ip_address=ip_address,
            protocol=protocol,
            mac_address=mac_address,
            status=status_port,
            service=service,
            port_id=port_id
        )
        status_attack = self.multiprocessing_attack_wrapper.arp_spoofing(
            ip_target=ip_address,
            ip_gateway=ip_gateway,
            verbose=True
        )
        attack.target = target
        attack.contex = "The attack was done with scapy"
        attack.status = status_attack
        return attack
