from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os, datetime
from pymongo import MongoClient

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
client = MongoClient(mongo_uri)

class TodoListView(APIView):

    def get(self, request):
        # Implement this method - return all todo items from db instance above.
        db = client['todo_db']
        todo_collection = db['todos']
        todos = list(todo_collection.find().sort('created_at', 1))
        todos = [str(todo['_id']) for todo in todos]
        return Response(todos, status=status.HTTP_200_OK)
        
    def post(self, request):
        # Implement this method - accept a todo item in a mongo collection, persist it using db instance above.
        db = client['todo_db']
        todo_collection = db['todos']
        todo_item = request.data
        todo_item['created_at'] = datetime.datetime.now() 
        result = todo_collection.insert_one(todo_item)
        return Response({"inserted_id": str(result.inserted_id)}, status=status.HTTP_200_OK)
     

