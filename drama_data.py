import json
from dataclasses import dataclass

@dataclass
class Drama:
    body: str
    headline: str | None
    image_url: str | None

@dataclass
class DramaTemplate:
    sentences: list[str]
    combinations: dict[str, list[str]]
    descriptions: dict[str, str]

    @staticmethod
    def from_file(path: str) -> "DramaTemplate":
        with open(path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            sentences = json_data["sentences"]
            combinations = json_data["combinations"]
            descriptions = json_data["descriptions"]
            return DramaTemplate(sentences=sentences, combinations=combinations, descriptions=descriptions)