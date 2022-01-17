from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .credentials_database import *


def main(request):
    return render(request, "welcomes/home.html")

def users(request):
    return render(request, "users/users.html")

@csrf_exempt 
def createNewUser(request):
    """
    Verifies that user doesn't exist in the db
    and creates the user, otherwise returns data 
    associated with a given email/username
    """

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        if not username or not email:
            return JsonResponse({'status': f'You have just submitted the wrong data: username="{username}", email="{email}"'})

        client = MongoClient(CONNECTION_STRING)
        database = client[DATABASE]
        collection = database[COLLECTION]

        if collection.find_one(filter={'email': email, 'username': username}):
            # return data about the user
            response = {
                'first_time': False,
                'username': username,
                'email': email
            }
            return JsonResponse(response)
        collection.insert_one({
            'username': username,
            'email': email
        })

        response = {
            'first_time': True,
            'username': username,
            'email': email
        }
        return JsonResponse(response)
