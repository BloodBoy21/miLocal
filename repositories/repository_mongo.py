# create father class for repositories
from typing import Type
from database.mongo import database
from pydantic import BaseModel


class RepositoryMongo:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, model: Type[BaseModel], collection: str):
        self.model = model
        self.collection = database.get_collection(collection)

    async def create(self, doc: Type[BaseModel]) -> BaseModel:
        try:
            return await self.collection.insert_one(doc.dict())
        except:
            raise

    def find_one(self, query: dict) -> BaseModel:
        return self.collection.find_one(query)
