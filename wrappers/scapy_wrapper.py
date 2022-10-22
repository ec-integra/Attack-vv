from scapy.all import sr1, IP, ICMP, Ether, ARP, srp
from models import ArpTableItem


class ScapyWrapper:
    def get_ip_gateway(self) -> str:
        packet = sr1(IP(dst="www.slashdot.org", ttl=0) / ICMP() / "XXXXXXXXXXX")
        return packet.src

    def arp_scan(self, ip) -> list[ARP]:
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        answers_packets, unanswered_packets = srp(request, timeout=2, retry=1)
        result = []

        for sent, received in answers_packets:
            arp_table_item = ArpTableItem()
            arp_table_item.ip_address = received.psrc
            arp_table_item.mac_address = received.hwsrc
            result.append(arp_table_item)

        return result
