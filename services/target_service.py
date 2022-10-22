from models import Target, Host, ArpTableItem
from constants import services_on_ports_for_brute_force

class TargetService:
    def create_target(
            self,
            ip_address: str,
            mac_address: str,
            port_id: str,
            status: str,
            service: str,
            protocol: str,
    ):
        target = Target()
        target.ip_address = ip_address
        target.mac_address = mac_address
        target.port_id = port_id
        target.status = status
        target.service = service
        target.protocol = protocol
        return target

    def cast_arp_table_in_targets(self, arp_table: list[ArpTableItem]) -> list[Target]:
        result = []
        for item in arp_table:
            target = self.create_target(
                item.ip_address,
                item.mac_address,
                port_id=None,
                status=None,
                service=None,
                protocol='arp'
            )
            result.append(target)
        return result

    def cast_hosts_in_targets(self, hosts: list[Host]) -> list[Target]:
        result = []
        for item in hosts:
            for port in item.ports:
                target = self.create_target(
                    item.ip_address,
                    item.mac_address,
                    port.port_id,
                    port.status,
                    port.service,
                    port.protocol
                )
                result.append(target)
        return result

    def cast_hosts_in_targets_brute_force(self, hosts: list[Host]) -> list[Target]:
        result = []
        for item in hosts:
            for port in item.ports:
                service_on_ports = port.service
                if service_on_ports in services_on_ports_for_brute_force:
                    target = self.create_target(
                        item.ip_address,
                        item.mac_address,
                        port.port_id,
                        port.status,
                        port.service,
                        port.protocol
                    )
                    result.append(target)
        return result

