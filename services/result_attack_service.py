class ResultAttackService:

    def check_status_attack(self, type_attack: str, report: str) -> bool:
        type_to_func_mapping = {
            "syn_flood": self.__check_success_syn_flood_attack,
            "udp_flood": self.__check_success_udp_flood_attack,
            "brute_force": self.__check_success_brute_force_attack
        }
        return type_to_func_mapping[type_attack](report)

    def __check_success_syn_flood_attack(self, report: str) -> bool:
        list_report = report.split('\n')[1:]
        flag = ''
        for data in list_report:
            for item in data.split(' '):
                if 'flags' in item:
                    chunks = item.split('=')
                    flag = chunks[1]
        return flag == 'SA'

    def __check_success_udp_flood_attack(self, report: str) -> bool:
        list_report = report.split('\n')
        list_icmp_responses = []
        for data in list_report:
            if "ICMP Port Unreachable" in data:
                list_icmp_responses.append(data)

        return len(list_icmp_responses) == 0

    def __check_success_brute_force_attack(self, report: str) -> bool:
        list_report = report.split('\n')
        for data in list_report:
            if "target successfully completed" in data:
                return True
        return False
