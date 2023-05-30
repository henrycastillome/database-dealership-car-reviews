from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.



def about(request):
    context={}
    if request.method=="GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context={}
    if request.method=="GET":
        return render(request, 'djangoapp/contact.html', context)


    
def login_request(request):
    context={}
    if request.method=='GET':
        return render(request, 'djangoapp/login.html', context)
    
    elif request.method=="POST":
        username= request.POST['username']
        password= request.POST['psw']
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message']='invalid username or password'
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method=="GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method=="POST":
        username=request.POST['username']
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        password=request.POST['psw']
        user_exist=False
        try:
            User.objects.get(username=username)
            user_exist=True
        except:
            logger.error("New User")
        if not user_exist:
            user=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message']="user already exist"
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership'
        dealerships=get_dealers(url)
        
        
        

        return render(request, 'djangoapp/index.html', context={'dealers':dealerships})

def get_dealer_details(request):
    context={}
    if request.method=="GET":
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-review'
        reviews=get_dealers_reviews(url)
        review_name=" ".join([rev.purchase_date for rev in reviews if rev.purchase_date is not None])

        return HttpResponse(review_name)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

