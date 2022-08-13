from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

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
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

