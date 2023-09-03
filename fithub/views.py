import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.urls import reverse
from .models import User, FoodLog, WeightLog


def index(request):
    return render(request, "fithub/index.html")

def authentication(request):
    return render(request, "fithub/authentication.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('authentication')
    else:
        return redirect('authentication')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2 or username == "":
            return redirect('authentication')
        
        try:
            user = User.objects.create_user(username = username, password = password)
            user.save()

            login(request, user)
        except IntegrityError:
            return redirect('authentication')
        return redirect('index')
    else:
        return redirect('authentication')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def edit_profile(request, user_id):
    try:
        user = User.objects.get(id = int(user_id))
    except User.DoesNotExist:
        return JsonResponse({"error":"User not found"}, status=404)
    
    if request.user != user:
        return redirect('index')
    
    if request.method == 'PUT':
        data = json.loads(request.body)

        if data.get('gender') is not None:
            user.gender = data['gender'].capitalize()
        
        if data.get('age') is not None:
            user.age = data['age']

        if data.get('height') is not None:
            user.height = data['height']

        if data.get('starting_weight') is not None:
            user.starting_weight = data['starting_weight']

        user.save()

        return HttpResponse(status=204)
    
    return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def user_info(request, user_id):
    try:
        user = User.objects.get(id = int(user_id))
    except User.DoesNotExist:
        return JsonResponse({"error" : "User not found"}, status=404)
    
    if request.user != user:
        return redirect('index')
    
    if request.method == 'GET':
        return JsonResponse({
            "id" : user.id,
            "username" : user.username,
            "date_joined" : user.date_joined,
            "age" : user.age,
            "starting_weight" : user.starting_weight,
            "current_weight" : user.current_weight,
            "height" : user.height,
            "gender" : user.gender,
            "activity" : user.activity,
            "objective" : user.objective,
            "bmr" : user.bmr,
            "daily_calories" : user.daily_calories
        })
    
    return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)