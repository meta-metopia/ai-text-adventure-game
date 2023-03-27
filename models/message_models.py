from dataclasses import dataclass
from enum import Enum
from typing import Optional

from jinja2 import Environment

from utils.get_selections import GameMessageWithSelections


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class PostMessageDto:
    content: str


@dataclass
class CreateMessageDto:
    role: Role
    content: str
    audio: Optional[str]
    image: Optional[str]

    def render(self, extra_data: Optional[dict] = None, inplace = True) -> str:
        """
        Render a message with extra data
        :param message: message
        :param extra_data: extra data
        :return:
        """
        if extra_data is None:
            return self.content
        env = Environment()
        template = env.from_string(self.content)
        if inplace:
            self.content = template.render(**extra_data)
            return self.content
        return template.render(**extra_data)

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "image": self.image,
            "audio": self.audio
        }

    def to_chat_gpt_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
        }


@dataclass
class GetMessageDto:
    role: Role
    content: str
    image: Optional[str]
    audio: Optional[str]

    @staticmethod
    def from_dict(data: dict) -> "GetMessageDto":
        return GetMessageDto(
            role=Role(data["role"]),
            content=data["content"],
            image=data.get("image"),
            audio=data.get("audio")
        )

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "image": self.image,
            "audio": self.audio
        }

    def to_chat_gpt_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
        }


@dataclass
class ChatMessageResponseDto(GameMessageWithSelections):
    audio: Optional[str]
    image: Optional[str]
