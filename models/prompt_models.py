from dataclasses import dataclass
from typing import Optional


@dataclass
class CreatePromptDto:
    """
    Create prompt dto
    """
    name: str
    prompt: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt
        }

    @staticmethod
    def from_dict(data: dict) -> "CreatePromptDto":
        return CreatePromptDto(
            name=data["name"],
            prompt=data["prompt"]
        )


@dataclass
class GetPromptDto:
    """
    Get prompt dto
    """
    name: str
    prompt: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt
        }

    @staticmethod
    def from_dict(data: dict) -> "GetPromptDto":
        return GetPromptDto(
            name=data["name"],
            prompt=data["prompt"]
        )


@dataclass
class UpdatePromptDto:
    """
    Update prompt dto
    """
    name: Optional[str]
    prompt: Optional[str]

    def to_dict(self) -> dict:
        data = {}
        if self.name is not None:
            data["name"] = self.name

        if self.prompt is not None:
            data["prompt"] = self.prompt

        return data

    @staticmethod
    def from_dict(data: dict) -> "UpdatePromptDto":
        return UpdatePromptDto(
            name=data.get("name"),
            prompt=data.get("prompt")
        )
