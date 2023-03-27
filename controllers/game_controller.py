from typing import Optional

import openai
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection

from controllers.controller import Controller
from models.message_models import CreateMessageDto, Role, ChatMessageResponseDto
from models.session_models import GetGameSessionDto, CreateGameSessionDto
from utils.get_selections import get_selections


class GameController(Controller):

    def __init__(self, client: MongoClient):
        super().__init__(client=client)
        self.collection: Collection = self.db["game-sessions"]
        self.collection.create_index("user", unique=True)

    def delete_session(self, user_id: str):
        try:
            data = self.collection.delete_one({"user": user_id})
            if data is None:
                raise HTTPException(status_code=500, detail="Failed to delete session")
            return {"message": "Session deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_new_game_session(self, user_id: str, data: CreateGameSessionDto):
        try:
            self.__create_new_game_session__(user_id=user_id, data=data)
            return {"message": "Session created successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_history(self, user_id: str) -> GetGameSessionDto:
        """
        Get the history of the game session
        :param user_id:
        :return:
        """
        try:
            session = self.collection.find_one({"user": user_id})
            messages = []
            # Get the selections for each message
            for message in session['messages']:
                message_with_selections = get_selections(message['content'])
                message['content'] = message_with_selections
                messages.append(message)
            session['messages'] = messages
            return GetGameSessionDto.from_dict(session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def chat(self, user_id: str, message: Optional[str] = None,
             extra_data: Optional[dict] = None) -> ChatMessageResponseDto:
        """
        Chat with the bot
        :param user_id: user id
        :param message: message from the user
        :param extra_data: extra data to be used in the prompt. This is used to render the prompt
        :return:
        """
        previous_session = self.__get_previous_game_session__(user_id=user_id)
        user_message = CreateMessageDto(role=Role.USER, content=message, audio=None,
                                        image=None) if message is not None else None
        if previous_session is None:
            raise HTTPException(status_code=404, detail="No session found. Please create a new session.")
        # Prepare the messages for the GPT-3 API
        system_message = CreateMessageDto(role=Role.SYSTEM, content=previous_session.prompt.prompt, audio=None,
                                          image=None)
        system_message.render(extra_data=extra_data)

        messages = [system_message.to_chat_gpt_dict()] + [message.to_chat_gpt_dict() for message in
                                                          previous_session.messages]
        if user_message is not None:
            user_message.render(extra_data=extra_data)
            messages = messages + [user_message.to_chat_gpt_dict()]
            # Add the user message to the game session
            self.__add_message_to_game_session__(user_id=user_id, message=user_message)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=messages,
        )

        # Add the bot message to the game session
        bot_message = CreateMessageDto(role=Role.ASSISTANT, content=response['choices'][0]['message']['content'],
                                       audio=None, image=None)
        self.__add_message_to_game_session__(user_id=user_id, message=bot_message)
        message_with_selection = get_selections(bot_message.content)
        return ChatMessageResponseDto(
            message=message_with_selection.message,
            selections=message_with_selection.selections,
            audio=None,
            image=None,
        )

    def __get_previous_game_session__(self, user_id: str) -> Optional[GetGameSessionDto]:
        """
        Get the previous game session for a user
        :param user_id: id
        :return:
        """
        try:
            session = self.collection.aggregate([
                {
                    '$match': {
                        'user': user_id
                    }
                }, {
                    '$lookup': {
                        'from': 'prompts',
                        'localField': 'prompt_name',
                        'foreignField': 'name',
                        'as': 'prompt'
                    }
                }, {
                    '$unwind': {
                        'path': '$prompt',
                        'includeArrayIndex': 'string',
                        'preserveNullAndEmptyArrays': True
                    }
                }
            ]).next()
            if session is None:
                return None
            return GetGameSessionDto.from_dict(session)
        except Exception as e:
            print("error: " + str(e))
            raise HTTPException(status_code=404, detail="No session found. Please create a new session.")

    def __create_new_game_session__(self, user_id: str, data: CreateGameSessionDto):
        """
        Create a new game session for a user
        :param user_id: id
        :return:
        """
        try:
            prompt_collection = self.db["prompts"]
            prompt = prompt_collection.find_one({"name": data.prompt_name})
            if prompt is None:
                raise HTTPException(status_code=404, detail="Prompt not found: " + data.prompt_name)
            data = self.collection.insert_one(data.to_dict(user=user_id))
            session = self.collection.find_one({"_id": data.inserted_id})
            if data is None:
                raise HTTPException(status_code=500, detail="Failed to create new game session")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def __add_message_to_game_session__(self, user_id: str, message: CreateMessageDto):
        """
        Add a message to a game session
        :param user_id: id
        :param message: message
        :return:
        """
        try:
            self.collection.update_one({"user": user_id}, {"$push": {"messages": message.to_dict()}})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
