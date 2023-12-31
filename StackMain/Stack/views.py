from django.shortcuts import render, redirect
from django.views import View
from Stack.classes.user import userClass
from .models import user, task
from Stack.classes.task import taskClass
from django.http import JsonResponse
import google.oauth2.id_token
import json
from django.views import View
from django.shortcuts import render, redirect
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core import serializers


# Create your views here.

class helpers():
    def redirectIfNotLoggedIn(request):
        if len(request.session.items()) == 0:
            return True
        if request.session["username"] is None:
            return True
        else:
            return False

class login(View):

    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        if 'forgot_password' in request.POST:
            return redirect("/password_reset/")
        

        noSuchUser = False
        blankName = False
        badPassword = False

        try:
            email = request.POST['email']
            currentUser = user.objects.get(email=email)
            password = request.POST['InputPassword']
            password = userClass.hashPass(password)
            badPassword = (currentUser.password != password)
        except Exception as e:
            noSuchUser = True

        if noSuchUser:
            return render(request, "login.html", {"error_message": "No such user exists!"})

        elif badPassword:
            return render(request, "login.html", {"error_message": "Incorrect password!"})
        else:
            request.session["username"] = currentUser.email
            # request.session["name"] = user.name
            return redirect("/tasks/")
    

class signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        try:
            userClass.createUser(self, firstName, lastName, email, password, confirmPassword)
            return render(request, "signup.html",
                          {'success_message': "User successfully created!"})
        except Exception as e:
            return render(request, "signup.html", {'error_message': str(e)})
        
class tasks(View):
    def get(self, request):
        if helpers.redirectIfNotLoggedIn(request):
             return redirect("/")

        currentSessionEmail = request.session["username"]
        currentUser = user.objects.get(email=currentSessionEmail)
        return render(request, "tasks.html", {"currentUser": currentUser})
        

class dbTask(View):
    def get(self, request):
        currentSessionEmail = request.session["username"]
        currentUser = user.objects.get(email=currentSessionEmail)
        allTasks = serializers.serialize('python', task.objects.filter(user = currentUser))
        response_data ={"tasks": [task["fields"] for task in allTasks]}
        return JsonResponse(response_data)
    
    def post(self, request):
        currentSessionEmail = request.session["username"]
        currentUser = user.objects.get(email=currentSessionEmail)
        taskData = json.loads(request.body)
        name = taskData['name']
        description = taskData['description']
        recurring = taskData['recurring']
        time = taskData['time']
        lock = False
        taskClass.createTask(self, name, description, lock, recurring, time, currentUser)
        allTasks = serializers.serialize('python', task.objects.filter(user = currentUser))
        response_data ={"message": "Task successfully created!", "tasks": [task["fields"] for task in allTasks]}
        return JsonResponse(response_data)



def google_auth_callback(request):
    # Retrieve the ID token from the client-side (you should validate this)
    id_token = request.POST.get('id_token')

    # Verify the ID token using the Google API client library
    try:
        # Verify the ID token using your Google API Client ID
        # Replace 'YOUR_CLIENT_ID' with your actual client ID
        id_info = google.oauth2.id_token.verify_oauth2_token(
            id_token, None
        )

        # Get the user's email and other information from id_info
        user_email = id_info['email']
        
        # You can now create a session for the user or perform other actions
        # like database lookups to check if the user exists in your system.

        # Redirect the user to the tasks page or wherever you need them to go.
        return redirect("/tasks/")
    except ValueError as e:
        # Handle verification error (e.g., invalid token)
        return JsonResponse({"error": "Invalid token"})

    # Handle other exceptions and errors as needed
    return JsonResponse({"error": "An error occurred"})