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

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import requests
import asyncio

param={
    "COUCH_URL":os.environ.get('COUCH_URL'),
    "IAM_API_KEY":os.environ.get('IAM_API_KEY')
}

def authentication(param_dict):
    authenticator=IAMAuthenticator(param_dict["IAM_API_KEY"])
    client=CloudantV1(authenticator=authenticator)
    client.set_service_url(param_dict['COUCH_URL'])
    
    return client


async def main(argv=None):
    try:
        client = authentication(param)
        response = await asyncio.to_thread(client.post_all_docs, db='reviews', include_docs=True).get_result()
        print(response)
        return {'body': response['rows']}
    except ApiException as cloudant_exception:
        print('unable to connect')
        return {'error': cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print('connection error')
        return {'error': err}
    
    
        
    return { 'body': response['rows'] }
    
    

    
    


