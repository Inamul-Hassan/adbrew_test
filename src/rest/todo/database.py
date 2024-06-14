from abc import ABC, abstractmethod
from typing import List, Dict
from pymongo import MongoClient
import os
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoDatabase(ABC):
    @abstractmethod
    def get_todos(self) -> List[Dict]:
        pass

    @abstractmethod
    def add_todo(self, todo_item: Dict) -> str:
        pass

class MongoDbTodo(TodoDatabase):
    def __init__(self):
        mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
        self.client = MongoClient(mongo_uri)
        self.db = self.client['todo_db']
        # Delete the collection to reset the database [Testing Purpose]
        # self.db.drop_collection('todos')
        self.todo_collection = self.db['todos']
        
        

    def get_todos(self) -> List[Dict]:
      """
      This method retrieves all todo items from the MongoDB.
      """
      try:
        todos = list(self.todo_collection.find().sort('created_at', 1))
        for todo in todos:
            todo['_id'] = str(todo['_id'])
        return todos
      except Exception as e:
        logger.error(f"Error retrieving todos: {e}")
        raise


    def add_todo(self, todo_item: Dict) -> str:   
      """
      This method accepts a todo item and persists it to the MongoDB.
      """   
      try:
        # adding created_at field for sorting the todo list
        todo_item['created_at'] = datetime.datetime.now()
        result = self.todo_collection.insert_one(todo_item)
        return str(result.inserted_id)
      except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise
