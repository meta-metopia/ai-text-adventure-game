from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from models.message_models import CreateMessageDto, GetMessageDto
from models.prompt_models import GetPromptDto


@dataclass
class CreateGameSessionDto:
    prompt_name: str

    def to_dict(self, user: str) -> dict:
        return {
            "user": user,
            "prompt_name": self.prompt_name,
            "messages": [],
            "created_at": datetime.now()
        }


@dataclass
class GetGameSessionDto:
    """
    User id
    """
    user: str
    messages: List[CreateMessageDto]
    prompt: Optional[GetPromptDto]

    @staticmethod
    def from_dict(data: dict) -> "GetGameSessionDto":
        return GetGameSessionDto(
            user=data["user"],
            messages=[GetMessageDto.from_dict(message) for message in data["messages"]],
            prompt=GetPromptDto.from_dict(data.get("prompt")) if data.get("prompt") is not None else data.get(
                "prompt_name")
        )
