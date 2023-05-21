#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import json
from ibmcloudant.cloudant_v1 import Document,CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import requests

param={
    "COUCH_URL":os.environ.get('COUCH_URL'),
    "IAM_API_KEY":os.environ.get('IAM_API_KEY')
}

def authentication(param_dict):
    authenticator=IAMAuthenticator(param_dict["IAM_API_KEY"])
    client=CloudantV1(authenticator=authenticator)
    client.set_service_url(param_dict['COUCH_URL'])
    
    return client
    
    

    
def nextId(client):
    response= client.post_all_docs(db='reviews', include_docs=True).get_result()
    next_id=max(int(doc['doc']['review_id']) for doc in response['rows']) + 1
    
    return next_id
     
 


def main(review):
   
    try:
        client= authentication(param)
        next_id=nextId(client)
        review = review['reviews']
       
        
        review_doc= Document(
            review_id=next_id,
            name=review['name'],
            dealership=review['dealership'],
            review=review['review'],
            purchase=review['purchase'],
            purchase_date=review['purchase_date'],
            car_make=review['car_make'],
            car_model=review['car_model'],
            car_year=review['car_year'],
            )
        response=client.post_document(db='reviews', document=review_doc).get_result()
        print(response)
    
    except ApiException as cloudant_exception:
        print('unable to connect')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(cloudant_exception)}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print('connection error')
        return {
            'statusCode': 503,
            'body': json.dumps({'error': str(err)}),
            'headers': {'Content-Type': 'application/json'}
        }
        
    
    
        
    return { 
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {'Content-Type': 'application/json'}
    }




