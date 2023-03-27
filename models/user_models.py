from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T')


@dataclass
class CreateUserDto:
    name: str
    password: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "password": self.password
        }


@dataclass
class GetUserDto:
    name: str
    password: str


@dataclass
class LoginDto:
    name: str
    password: str
