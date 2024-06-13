from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
import logging

from .database import TodoDatabase, MongoDbTodo


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todo_database: TodoDatabase = MongoDbTodo()

    def get(self, request):
        """
        Retrieve all todo items from the database.
        """
        try:
            todos = self.todo_database.get_todos()
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
                raise ValueError("The 'todo' field is required in the request.")
            inserted_id = self.todo_database.add_todo(todo_item)
            return Response({"inserted_id": inserted_id}, status=status.HTTP_201_CREATED)
        
        except ParseError as pe:
            logger.error(f"Error creating todo: {pe}")
            return Response({"error": "Invalid JSON format."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            logger.error(f"Error creating todo: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            return Response({"error": "Failed to create todo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
