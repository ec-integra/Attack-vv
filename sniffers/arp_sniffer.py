from scapy.all import sniff


class ArpSniffer:
    def __init__(self):
        self.ip_mac_dict = {}
        self.status_attacks = []

    # Возвращает True в случае обнаружении атаки
    # False в случае неуспешной атаки
    def get_status_arp_spoofing(self):
        count_successful_attacks = self.status_attacks.count(True)
        count_unsuccessful_attacks = self.status_attacks.count(False)
        return count_successful_attacks > count_unsuccessful_attacks

    def packet_sniff(self, packet):
        ip_source = packet['ARP'].psrc
        mac_source = packet['Ether'].src
        if mac_source in self.ip_mac_dict.keys():
            if self.ip_mac_dict[mac_source] != ip_source:
                try:
                    ip_reference = self.ip_mac_dict[mac_source]
                except:
                    ip_reference = "unknown"

                print(f'\n[+] Обнаружена возможная ARP-атака\n'
                      f'- Возможно, что машина с адресом\n- {ip_reference} '
                      f'притворяется {ip_source}\n')
                self.status_attacks.append(True)
        else:
            self.ip_mac_dict[mac_source] = ip_source
            self.status_attacks.append(False)


def do_arp_sniffer(condition_container: dict):
    arp_sniffer = ArpSniffer()
    sniff(count=30, filter="arp", store=1, prn=arp_sniffer.packet_sniff)
    condition_container["condition_sniffer"] = arp_sniffer.get_status_arp_spoofing()
