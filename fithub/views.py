import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.urls import reverse
from .models import User, FoodLog, WeightLog
import datetime


def index(request):
    return render(request, "fithub/index.html", {
        "calories" : 0,
        "date" : datetime.datetime.now()
    })

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
            user.current_weight = data['starting_weight']

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

def edit_nutrition(request, user_id):
    try:
        user = User.objects.get(id = int(user_id))
    except User.DoesNotExist:
        return JsonResponse({"error":"User not found"}, status=404)
    
    if request.user != user:
        return redirect('index')
    
    if request.method == 'PUT':
        data = json.loads(request.body)

        if data.get('objective') is not None:
            user.objective = data['objective']
        
        if data.get('activity') is not None:
            user.activity = data['activity']

        if data.get('bmr') is not None:
            user.bmr = data['bmr']

        if data.get('daily_calories') is not None:
            user.daily_calories = data['daily_calories']

        user.save()

        return HttpResponse(status=204)
    
    return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def clear(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return redirect('index')

    if request.user != user:
        return redirect('index')
    
    user.age = 0
    user.starting_weight = 0
    user.current_weight = 0
    user.height = 0
    user.gender = ""
    user.activity = ""
    user.objective = ""
    user.bmr = 0
    user.daily_calories = 0
    user.save()
    
    wlogs = WeightLog.objects.filter(user = user)
    flogs = FoodLog.objects.filter(user = user)

    for i in wlogs:
        i.delete()
    for i in flogs:
        i.delete()
    
    return redirect('index')