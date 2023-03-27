import logging
import os
from typing import Optional

import boto3
import certifi
import openai
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasicCredentials
from pymongo import MongoClient

from auth import generate_token, JWTBearer, admin_auth
from controllers.game_controller import GameController
from controllers.prompt_controller import PromptController
from controllers.user_controller import UserController
from models.message_models import PostMessageDto
from models.prompt_models import CreatePromptDto, UpdatePromptDto
from models.session_models import CreateGameSessionDto
from models.user_models import CreateUserDto, LoginDto

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

db_url = os.getenv("DB_URL")
endpoint_url = os.getenv("AWS_ENDPOINT_URL")
public_url = os.getenv("PUBLIC_URL")
bucket_name = os.getenv("AWS_BUCKET_NAME")
region_name = os.getenv("AWS_REGION_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
open_ai_key = os.getenv("OPENAI_API_KEY")

logging.info(f"DB_URL: {db_url}")
logging.info(f"AWS_ENDPOINT_URL: {endpoint_url}")
logging.info(f"PUBLIC_URL: {public_url}")
logging.info(f"AWS_BUCKET_NAME: {bucket_name}")
logging.info(f"AWS_REGION_NAME: {region_name}")
logging.info(f"AWS_ACCESS_KEY_ID: {aws_access_key_id}")
logging.info(f"AWS_SECRET_ACCESS_KEY: {aws_secret_access_key}")

mongo_client = MongoClient(db_url, tlsCAFile=certifi.where() if db_url.startswith("mongodb+srv") else None)
openai.api_key = open_ai_key
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=region_name,
                         endpoint_url=endpoint_url,
                         )

# controller
user_controller = UserController(client=mongo_client)
game_controller = GameController(client=mongo_client)
prompt_controller = PromptController(client=mongo_client)


@app.post("/login")
def login(user: LoginDto):
    """
    Login a user
    """
    user = user_controller.login(credentials=user)
    token = generate_token(data={"name": user["name"], "id": str(user["_id"])})
    return {"access_token": token}


@app.post("/register")
def register(user: CreateUserDto):
    """
    Register a new user
    :param user: user to register
    :return:
    """
    user_controller.register(user=user)
    return {"message": "User registered successfully"}


@app.post("/prompt")
def create_prompt(data: CreatePromptDto, credentials: HTTPBasicCredentials = Depends(admin_auth)):
    return prompt_controller.add_new_prompt(prompt=data)


@app.get("/prompt/{name}")
def get_prompt(name: str):
    return prompt_controller.get_prompt(prompt_name=name)


@app.get("/prompt")
def get_all_prompts():
    return prompt_controller.get_all_prompts()


@app.patch("/prompt/{name}")
def update_prompt(name: str, data: UpdatePromptDto, credentials: HTTPBasicCredentials = Depends(admin_auth)):
    return prompt_controller.update_prompt(prompt_name=name, prompt=data)


@app.delete("/prompt/{name}")
def delete_prompt(name: str, credentials: HTTPBasicCredentials = Depends(admin_auth)):
    return prompt_controller.delete_prompt(prompt_name=name)


@app.post("/chat/new")
def new_chat(data: CreateGameSessionDto, user: dict = Depends(JWTBearer())):
    user_id = user["id"]
    return game_controller.create_new_game_session(user_id=user_id, data=data)


@app.post("/chat")
def chat(data: Optional[PostMessageDto] = None, user: dict = Depends(JWTBearer())):
    user_id = user["id"]
    extra_data = {
        "name": user["name"],
    }
    if data is None:
        return game_controller.chat(user_id=user_id, message=None, extra_data=extra_data)
    return game_controller.chat(user_id=user_id, message=data.content, extra_data=extra_data)


@app.delete("/chat")
def delete_chat(user: dict = Depends(JWTBearer())):  # type: ignore
    user_id = user["id"]
    return game_controller.delete_session(user_id=user_id)


@app.get("/chat")
def get_chat(user: dict = Depends(JWTBearer())):  # type: ignore
    user_id = user["id"]
    return game_controller.get_history(user_id=user_id)
