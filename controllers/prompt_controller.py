from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection

from controllers.controller import Controller
from models.prompt_models import CreatePromptDto, GetPromptDto, UpdatePromptDto


class PromptController(Controller):
    def __init__(self, client: MongoClient):
        super().__init__(client=client)
        self.collection: Collection = self.db["prompts"]
        self.collection.create_index("name", unique=True)

    def add_new_prompt(self, prompt: CreatePromptDto):
        """
        Add a new prompt
        :param prompt: prompt to add
        :return:
        """
        try:
            data = self.collection.insert_one(prompt.to_dict())
            if data is None:
                raise HTTPException(status_code=500, detail="Failed to add prompt")
            return {"message": "Prompt added successfully"}

        except Exception as e:
            if "E11000" in str(e):
                raise HTTPException(status_code=400, detail="Prompt already exists")
            raise HTTPException(status_code=500, detail=str(e))

    def get_prompt(self, prompt_name: str):
        """
        Get a prompt
        :param prompt_name: prompt name
        :return:
        """
        try:
            prompt = self.collection.find_one({"name": prompt_name})
            if prompt is None:
                raise HTTPException(status_code=404, detail="Prompt not found")
            return GetPromptDto.from_dict(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_prompts(self):
        """
        Get all prompts
        :return:
        """
        try:
            prompts = self.collection.find()
            if prompts is None:
                raise HTTPException(status_code=404, detail="No prompts found")
            return [GetPromptDto.from_dict(prompt) for prompt in prompts]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_prompt(self, prompt_name: str, prompt: UpdatePromptDto):
        try:
            self.collection.update_one({"name": prompt_name}, {"$set": prompt.to_dict()})
            return {"message": "Prompt updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_prompt(self, prompt_name: str):
        try:
            self.collection.delete_one({"name": prompt_name})
            return {"message": "Prompt deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
