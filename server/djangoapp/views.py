from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarModel, CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid credentials."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):

    context = {}

    if request.method == 'POST':

        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
            
        if not user_exist:
            user = User.objects.create_user(

                username=username, 
                first_name=first_name, 
                last_name=last_name,
                password=password
            )
            
            login(request, user)
            return redirect("djangoapp:index")
        
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
    
    else:
        return render(request, 'djangoapp/registration.html', context)
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://a8b45b9f.eu-gb.apigw.appdomain.cloud/dealership"
        # Get dealers from the URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', {'dealerships': dealerships})

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId):
    if request.method == "GET":
        # Get dealers from the URL
        url = f'https://a8b45b9f.eu-gb.apigw.appdomain.cloud/api/review/?dealerId={dealerId}'
        reviews = get_dealer_by_id_from_cf(url, dealerId)
        for i in range(len(reviews)):
            reviews[i].sentiment = reviews[i].sentiment.capitalize()

        
        url_dealerships = "https://a8b45b9f.eu-gb.apigw.appdomain.cloud/dealership"
        dealerships = get_dealers_from_cf(url_dealerships)
        for dealer in dealerships:
            if dealerId == dealer.id:
                return render(request, 'djangoapp/dealer_details.html', {'dealer': dealer, 'reviews': reviews})

# Create a `add_review` view to submit a review
def add_review(request, dealerId):
    if request.method == "GET":
        cars = CarModel.objects.all()
        # filter by dealerId
        cars = cars.filter(dealer_id=dealerId)
        url_dealerships = "https://a8b45b9f.eu-gb.apigw.appdomain.cloud/dealership"
        dealerships = get_dealers_from_cf(url_dealerships)
        dealer_info = []
        for dealer in dealerships:
            if dealerId == dealer.id:
                dealer_info.append(dealer)
        print(dealer_info)
        return render(request, 'djangoapp/add_review.html', {'dealerId': dealerId, 'cars': cars})
    else:
        

        # Get the posted form data
        first_name = User.objects.get(username=request.user).first_name
        last_name = User.objects.get(username=request.user.username).last_name
        name = first_name + " " + last_name

        review = {
            "id": dealerId,
            "name": name,
            "review": request.POST.get("content"),
            "purchase": request.POST.get("purchasecheck"),
            "car": request.POST.get("car"),
            "purchase_date": request.POST.get("purchasedate"),
            "time": datetime.utcnow().isoformat(),
            "dealership": dealerId,
        }

        json_payload = {"review": review}

        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/Mohitshi%40icloud.com_djangoserver-space/default/post_review"
        req = post_request(url, json_payload)
        return redirect('djangoapp:dealer_details', dealerId=dealerId)

# https://a8b45b9f.eu-gb.apigw.appdomain.cloud/api/dealership?state=CA
# https://a8b45b9f.eu-gb.apigw.appdomain.cloud/api/review/?dealerId=1
# https://a8b45b9f.eu-gb.apigw.appdomain.cloud/dealership
# https://a8b45b9f.eu-gb.apigw.appdomain.cloud/api/review/
# https://eu-gb.functions.appdomain.cloud/api/v1/web/Mohitshi%40icloud.com_djangoserver-space/default/post_review
