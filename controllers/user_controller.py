from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection

from controllers.controller import Controller
from models.user_models import CreateUserDto, LoginDto


class UserController(Controller):
    def __init__(self, client: MongoClient):
        super().__init__(client=client)
        self.collection: Collection = self.db["users"]
        self.collection.create_index("name", unique=True)

    def register(self, user: CreateUserDto):
        """
        Register a new user
        :param user: user to register
        :return:
        """
        try:
            data = self.collection.insert_one(user.to_dict())
            if data is None:
                raise HTTPException(status_code=500, detail="Failed to register user")
            return data

        except Exception as e:
            if "E11000" in str(e):
                raise HTTPException(status_code=400, detail="User already exists")
            raise HTTPException(status_code=500, detail=str(e))

    def login(self, credentials: LoginDto):
        """
        Login a user
        :param credentials: user credentials
        :return:
        """
        try:
            user = self.collection.find_one({"name": credentials.name, "password": credentials.password})
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
