from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection

from controllers.controller import Controller
from models.prompt_models import CreatePromptDto, GetPromptDto, UpdatePromptDto, ListPromptDto


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
        prompt = self.collection.find_one({"name": prompt_name})
        if prompt is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return GetPromptDto.from_dict(prompt)

    def get_all_prompts(self):
        """
        Get all prompts
        :return:
        """
        prompts = self.collection.find()
        if prompts is None:
            return HTTPException(status_code=404, detail="No prompts found")
        return ListPromptDto.from_list(prompts)

    def update_prompt(self, prompt_name: str, prompt: UpdatePromptDto):
        data = prompt.to_dict()
        updated_result = self.collection.update_one({"name": prompt_name}, {"$set": data})
        if updated_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return {"message": "Prompt updated successfully"}

    def delete_prompt(self, prompt_name: str):
        self.collection.delete_one({"name": prompt_name})
        return {"message": "Prompt deleted successfully"}

