import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions


load_dotenv()

param_nlu={
    "NLU_API_KEY":os.environ.get('NLU_API_KEY'),
    "NLU_URL":os.environ.get('NLU_URL')
}


def get_requests(url,kwargs=None, api_key=None):
    print(kwargs)
    print("GET from {}".format(url))
    response=None
    try:
        if api_key:
            response = requests.get(
                url, headers={'Content-Type': "application/json"}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
            
        else:
            response = requests.get(
                url, headers={'Content-Type': "application/json"}, params=kwargs)

    except requests.exceptions.RequestException as e:
        print("Error occurred during requests ", e)

    if response:

        status_code = response.status_code
        print("With status {}".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    
    return None

def post_requests_review(url, kwargs):
    print(kwargs)
    print("POST to {}".format(url))
   
    

    try:
        response=requests.post(url, headers={'Content-Type':'application/json'}, json=kwargs)
        status_code=response.status_code
        print("with status {}".format(status_code))
        json_data=response.json()
        print(json_data)
        return json_data
        

    except requests.exceptions.RequestException as e:
        print("error ocurred during requests", e)
    
  
        

    






def get_dealers(url, **kwargs):
    results = []
    json_results = get_requests(url)

    if json_results:
    
        for dealer in json_results:
            dealers=dealer['doc']
            dealer_object= CarDealer(id=dealers['id'], 
                                     full_name=dealers['full_name'], 
                                     address=dealers['address'], 
                                     city=dealers['city'], 
                                     st=dealers['st'],
                                     state=dealers['state'],
                                     zip=dealers['zip'])
            
            results.append(dealer_object)

    return results

def get_dealers_by_id(url, id):
    result=[]
    
    json_results= get_requests(url, id)
    if json_results:

        for dealers in json_results:
            dealer_object= CarDealer(id=dealers['id'], 
                                     full_name=dealers['full_name'], 
                                     address=dealers['address'], 
                                     city=dealers['city'], 
                                     st=dealers['st'],
                                     state=dealers['state'],
                                     zip=dealers['zip'])
            result.append(dealer_object)

        return result

def analyze_review_sentiments(review):

    try:
        authenticator=IAMAuthenticator(param_nlu['NLU_API_KEY'])
        service=NaturalLanguageUnderstandingV1(version='2002-04-07', authenticator=authenticator)
        service.set_service_url(param_nlu['NLU_URL'])
        response = service.analyze(text=review,  features=Features(
                        keywords=KeywordsOptions(emotion=True, sentiment=True))).get_result()
        if 'keywords' in response and len(response['keywords'])>0:

            sentiment=response['keywords'][0]['sentiment']['label']
            return sentiment
        else:
            sentiment='neutral'
            return sentiment
            


        
    except ApiException as cloudant_exception:
        print('unable to connect')
        return{
            'statusCode':500,
            'body':json.dumps({'error':str(cloudant_exception)}),
            'headers':{'Content-Type':'application/json'}
        }
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print('connection error')
        return{
            'statusCode':505,
            'body':json.dumps({'error':str(err)}),
            'headers':{'Content-Type':'application/json'}
        }
    
def get_dealers_reviews(url, **kwargs):
    results=[]
    json_results=get_requests(url)

    if json_results:
        for review in json_results:
            reviews=review['doc']
            review_to_analyze=reviews.get('review', '')
            analyze= analyze_review_sentiments(review_to_analyze)

            review_object= DealerReview(dealership=reviews['dealership'],
                                        name=reviews['name'],
                                        purchase=reviews['purchase'],
                                        review=reviews['review'],
                                        purchase_date=reviews.get('purchase_date'),
                                        car_make=reviews.get('car_make'),
                                        car_model=reviews.get('car_model'),
                                        car_year=reviews.get('car_year'),
                                        review_id=str(reviews['review_id']),
                                        sentiment=analyze)
            results.append(review_object)
    
    return results


def get_dealer_review_id(url, id):
    results=[]
    json_results=get_requests(url, id)

    if json_results:
        for reviews in json_results:
            
            review_to_analyze=reviews['review']
            analyze= analyze_review_sentiments(review_to_analyze)
            review_object= DealerReview(dealership=reviews['dealership'],
                                        name=reviews['name'],
                                        purchase=reviews['purchase'],
                                        review=reviews['review'],
                                        purchase_date=reviews.get('purchase_date'),
                                        car_make=reviews.get('car_make'),
                                        car_model=reviews.get('car_model'),
                                        car_year=reviews.get('car_year'),
                                        review_id=str(reviews['review_id']),
                                        sentiment=analyze)
            results.append(review_object)
    
    return results









