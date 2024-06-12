from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import os
import datetime
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Client Config
mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
client = MongoClient(mongo_uri)
db = client['todo_db']
# Clear the databse collection
# db.drop_collection('todos')
todo_collection = db['todos']

class TodoListView(APIView):

    def get(self, request):
        """
        Retrieve all todo items from the database.
        """
        try:
            todos = list(todo_collection.find().sort('created_at', 1))
            # If the collection is empty, return an empty list
            if len(todos) == 0:
                return Response([], status=status.HTTP_200_OK)
            
            # converting ObjectId to string
            for todo in todos:
                todo['_id'] = str(todo['_id'])
                
            return Response(todos, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error retrieving todos: {e}")
            return Response({"error": "Failed to retrieve todos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Accept a todo item and persist it to the database.
        """
        try:
            todo_item = request.data
            if not todo_item.get('todo'):
                logger.error("Error creating todo: 'todo' field is required.")
                return Response({"error": "The 'todo' field is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # adding created_at field for sorting the todo list
            todo_item['created_at'] = datetime.datetime.now()
            result = todo_collection.insert_one(todo_item)
            return Response({"inserted_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            return Response({"error": "Failed to create todo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
