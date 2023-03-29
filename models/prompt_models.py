from dataclasses import dataclass
from typing import Optional


@dataclass
class CreatePromptDto:
    """
    Create prompt dto
    """
    name: str
    prompt: str
    """
    First user message. If this is set, the first message will be sent with the prompt
    """
    first_user_message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt,
            "first_user_message": self.first_user_message
        }

    @staticmethod
    def from_dict(data: dict) -> "CreatePromptDto":
        return CreatePromptDto(
            name=data["name"],
            prompt=data["prompt"],
            first_user_message=data.get("first_user_message")
        )


@dataclass
class GetPromptDto:
    """
    Get prompt dto
    """
    name: str
    prompt: str
    first_user_message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt,
            "first_user_message": self.first_user_message
        }

    @staticmethod
    def from_dict(data: dict) -> "GetPromptDto":
        return GetPromptDto(
            name=data["name"],
            prompt=data["prompt"],
            first_user_message=data.get("first_user_message")
        )


@dataclass
class ListPromptDto:
    name: str

    @staticmethod
    def from_dict(data: dict) -> "ListPromptDto":
        return ListPromptDto(
            name=data["name"]
        )

    @staticmethod
    def from_list(data: list) -> list:
        return [ListPromptDto.from_dict(item) for item in data]


@dataclass
class UpdatePromptDto:
    """
    Update prompt dto
    """
    name: Optional[str] = None
    prompt: Optional[str] = None
    first_user_message: Optional[str] = None

    def to_dict(self) -> dict:
        data = {}
        if self.name is not None:
            data["name"] = self.name

        if self.prompt is not None:
            data["prompt"] = self.prompt

        if self.first_user_message is not None:
            data["first_user_message"] = self.first_user_message

        return data

    @staticmethod
    def from_dict(data: dict) -> "UpdatePromptDto":
        return UpdatePromptDto(
            name=data.get("name"),
            prompt=data.get("prompt"),
            first_user_message=data.get("first_user_message")
        )
