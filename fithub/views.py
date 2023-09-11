import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.urls import reverse
from .models import User, FoodLog, WeightLog
import datetime, pytz


def index(request):
    today = datetime.datetime.now()

    # most recent weight log
    id = sorted([log.id for log in WeightLog.objects.filter(user= request.user)])
    if len(id) > 0:
        id = id[-1]
    else:
        id = 0
    lasttimestamp = WeightLog.objects.filter(user = request.user, id = id)
    if len(lasttimestamp) != 0:
        weight = lasttimestamp[0].weight
        newweightlog = False
    else:
        newweightlog = True
        weight = 0
        percentage = 0
    if not newweightlog:
        diff = datetime.datetime.now() - lasttimestamp[0].timestamp.replace(tzinfo=None)
        newweightlog = diff.days >= 7

    # percentage lost
    start = request.user.starting_weight
    current = request.user.current_weight
    try:
        percentage = (current-start)/start * 100
    except ZeroDivisionError:
        percentage = 0
    if percentage >= 0:
        percentage = "+ " + "{:.2f}".format(percentage) + '%'
    else: 
        percentage = "- " + ("{:.2f}".format(percentage))[1:] + '%'


    # sum of calories
    flogs = []
    for log in FoodLog.objects.all():
        if log.user == request.user and log.timestamp.day == today.day and log.timestamp.month == today.month and log.timestamp.year == today.year:
            flogs.append(log)
    calories = sum([l.calories for l in flogs])


    return render(request, "fithub/index.html", {
        "newuser" : request.user.starting_weight == 0,
        "month" : datetime.datetime.today().strftime('%B'),
        "calories" : round(calories),
        "date" : today,
        "breakfast" : [log for log in flogs if log.meal == 'Breakfast'],
        "lunch" : [log for log in flogs if log.meal == 'Lunch'],
        "dinner" : [log for log in flogs if log.meal == 'Dinner'],
        "snacks" : [log for log in flogs if log.meal == 'Snacks'],
        "newweightlog" : newweightlog,
        "weight" : weight,
        "percentage" : percentage,
        "remove" : len(WeightLog.objects.filter(user = request.user))
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

        if not(data.get('gender') and data.get('age') and data.get('height') and data.get('starting_weight')):
            return HttpResponse(status=200)

        if data.get('gender') != "":
            user.gender = data['gender'].capitalize()
        
        if data.get('age') != "":
            user.age = data['age']

        if data.get('height') != "":
            user.height = data['height']

        if data.get('starting_weight') != "":
            user.starting_weight = data['starting_weight']
            user.current_weight = data['starting_weight']

        user.save()

        log = WeightLog(user = user, weight = data['starting_weight'])
        log.save()

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
        return HttpResponse(status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)

        if not(data.get('objective') and data.get('activity') and data.get('bmr') and data.get('daily_calories')):
            return HttpResponse(status=404)

        if data.get('objective') != "":
            user.objective = data['objective']
        
        if data.get('activity') != "":
            user.activity = data['activity']

        if data.get('bmr') != "":
            user.bmr = data['bmr']

        if data.get('daily_calories') != "":
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
        return HttpResponse(status=404)

    if request.user != user:
        return HttpResponse(status=404)
    
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


def add_food(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.user != user:
        return HttpResponse(status=404)
    
    if request.method == 'POST':
        data = json.loads(request.body)

        if not (data.get('name') and data.get('weight') and data.get('calories') and data.get('meal')):
            return HttpResponse(status = 404)
        
        if data.get('name') != "":
            name = data['name']
        
        if data.get('weight') != "":
            weight = data['weight']

        if data.get('calories') != "":
            calories = data['calories']
            calories = round(float(calories.split(' ')[0]))

        if data.get('meal') != "":
            meal = data['meal']

        food = FoodLog(user = user, name = name, weight = weight, calories = calories, meal = meal)
        food.save()

        return HttpResponse(status=204)

    return HttpResponse(status=404)


def remove_food(request, log_id):
    try:
        log = FoodLog.objects.get(id = log_id)
    except FoodLog.DoesNotExist:
        return HttpResponse(status=404)

    if request.user != log.user:
        return HttpResponse(status=404)
    
    log.delete()

    return redirect('index')


def add_weight(request, user_id, weight):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return redirect('index')

    if request.user != user or request.user.starting_weight == 0:
        return redirect('index')
    
    WeightLog(user = user, weight = float(weight)).save()

    return redirect('index')   


def remove_weight(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return redirect('index')

    if request.user != user:
        return redirect('index')
    
    id = sorted([log.id for log in WeightLog.objects.filter(user= request.user)])[-1]
    lastlog = WeightLog.objects.get(user = request.user, id = id)
    if len(WeightLog.objects.filter(user = user)) > 1:
        lastlog.delete()

    return redirect('index')   


from datetime import date, timedelta

def weight_data(request, user_id):
    try:
        user = User.objects.get(id=int(user_id))
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.user != user:
        return redirect('index')

    today = date.today()
    start_date = today.replace(day=1)
    end_date = start_date.replace(day=1, month=start_date.month + 1)

    weight_data_dict = {start_date + timedelta(days=i): None for i in range((end_date - start_date).days)}


    weight_logs = WeightLog.objects.filter(user=user, timestamp__gte=start_date, timestamp__lt=end_date).order_by('timestamp')

    for log in weight_logs:
        log_date = log.timestamp.date()
        weight_data_dict[log_date] = log.weight

    timestamps = [date.day  for date in weight_data_dict.keys()]
    weights = [weight_data_dict[date] for date in weight_data_dict.keys()]

    if request.method == 'GET':
        return JsonResponse({
            "timestamps": json.dumps(timestamps),
            "weights": json.dumps(weights)
        })

    return JsonResponse({
        "error": "GET or PUT request required."
    }, status=400)
