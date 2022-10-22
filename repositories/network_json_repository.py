import json


class NetworkJsonRepository:
    def parse_in_dict(self, filename: str) -> dict:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data