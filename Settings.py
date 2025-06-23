from dataclasses import dataclass

@dataclass
class Settings:
    primary_from: int
    primary_to: int
    production_from: int
    production_to: int
    page: int
    dromru_allowed: bool
    autoru_allowed:bool