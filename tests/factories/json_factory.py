from typing import Union
import json


class JsonFactory:
    Json = Union[dict, list]

    def __init__(self, base_path: str):
        self.base_path = base_path

    def load_json(self, path: str) -> Json:
        with open(f"{self.base_path}/{path}", "r") as file:
            content = json.load(file)
        return content
