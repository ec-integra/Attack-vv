from multiprocessing import Process, Manager
from attacks import do_arp_spoofing
from sniffers import do_arp_sniffer
from time import sleep


class MultiprocessingAttacksWrapper:
    def arp_spoofing(self, ip_target=str, ip_gateway=str, verbose=bool):
        manager = Manager()
        shared_dict = manager.dict()

        arp_spoofing_process = Process(
            target=do_arp_spoofing,
            args=(shared_dict, ip_target, ip_gateway, verbose, )
        )

        arp_sniffer_process = Process(target=do_arp_sniffer, args=(shared_dict, ))

        arp_spoofing_process.start()
        arp_sniffer_process.start()

        while True:
            sleep(3)
            if not shared_dict.get("condition_sniffer"):
                continue

            print(shared_dict)
            arp_sniffer_process.kill()
            print("kill sniffer process")
            arp_spoofing_process.kill()
            print("kill arp_spoofing process")
            return shared_dict.get("condition_sniffer")
