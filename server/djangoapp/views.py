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
import time

# Get an instance of a logger
logger = logging.getLogger(__name__)





def about(request):
    context={}
    if request.method=="GET":
        return render(request, 'djangoapp/about.html', context)




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



def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


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


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        count=0
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership'
        dealerships=get_dealers(url)
        results_count=[]
        for dealer in dealerships:
            count +=1
            results_count.append(count)
       
    
        context['dealerships']=len(results_count)
        context['dealers']=dealerships
        context['users']=User.objects.count()

        url_reviews='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-review'
        reviews=get_dealers_reviews(url_reviews)
        count_reviews=0
        count_result_review=[]

        for count in reviews:
            count_reviews+=1
            count_result_review.append(count_reviews)
        
        context['reviews']=len(count_result_review)


        
        
        

        return render(request, 'djangoapp/index.html', context=context)

def post_review(request, id):
    context={}
    if request.method=="GET":
        id={"id":id}
        url_get='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership-id'
        dealerships=get_dealers_by_id(url_get,id)
            
        return render(request, 'djangoapp/review_post.html', context={'dealerships':dealerships} )
    
    elif request.method=="POST":
        url_get='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership-id'
        url_post='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/post-review'
        name=request.POST.get('name', "")
        dealership=request.POST.get('dealershipid',"")
        car_make=request.POST['car_make']
        car_model=request.POST['car_model']
        car_year=request.POST['car_year']
        purchase_date=request.POST['purchase_date']
        purchase=request.POST['purchase']
        review=request.POST.get('review')
        

        if(purchase=='yes'):
            purchase=True
        else:
            purchase=False
        
        data_json={"reviews":
                   {
                       "name":name,
                       "dealership":int(dealership),
                       "car_make":car_make,
                       "car_model":car_model,
                       "car_year":int(car_year),
                       "purchase_date":purchase_date,
                       "purchase":purchase,
                       "review":review

                   }}
        id_get={"id":dealership}
        try:
            response = post_requests_review(url_post, data_json)
            
            
            print(response)
            if(response['ok']):
                

                context['message']='Your review has been posted'
                context['dealerships']= get_dealers_by_id(url_get, id_get)
                messages.success(request,"Your post has been posted")

                return redirect('djangoapp:dealer_details', id=dealership)
            else:
                context['message']='error in the server-- try again later'
                context['dealerships']= get_dealers_by_id(url_get, id_get)
                
                return render(request, 'djangoapp/review_post.html', context=context)
            
            
        except Exception as e:
            error_message = "An error occurred while posting the review: {}".format(str(e))
            context['message']=error_message
            context['dealerships']= get_dealers_by_id(url_get, id_get)
                
            return render(request, 'djangoapp/review_post.html', context=context)
            

    
def get_dealer_review(request, id):
    context={}
    if request.method=="GET":
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-review-id'
        id={"id":id}
        reviews=get_dealer_review_id(url, id)

        url2='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership-id'
        dealerships=get_dealers_by_id(url2,id)

        return render(request, 'djangoapp/dealer_details.html', context={"reviews":reviews, "dealerships":dealerships})
    
    






def get_dealer_id(request,id):
    context={}
    if request.method=='GET':
        id={"id":id}
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership-id'
        dealerships=get_dealers_by_id(url,id)
        response=" ".join([response.full_name for response in dealerships if response.full_name is not None])

        return HttpResponse(response)


def get_dealer_details(request):
    context={}
    if request.method=="GET":
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-review'
        reviews=get_dealers_reviews(url)
        review_name=" ".join([rev.purchase_date for rev in reviews if rev.purchase_date is not None])

        return HttpResponse(review_name)

    


def search_dealer(request):
    context = {}
    if request.method == "GET":
        keyword= request.GET.get('search', ' ')
        url='https://us-east.functions.appdomain.cloud/api/v1/web/bb38ac2a-c860-4a62-9d45-c9c576b3a2d0/dealership-package/get-dealership'
        dealerships=get_dealers(url)
        results=[]

        for dealer in dealerships:
            if keyword.lower() in dealer.full_name.lower() or \
               keyword.lower() in dealer.st.lower() or \
               keyword.lower() in dealer.state.lower() or \
               keyword.lower() in dealer.city.lower():
                results.append(dealer)

        context['dealers']=results
        context['keyword']=keyword
        
        
        

        return render(request, 'djangoapp/result.html', context=context)



