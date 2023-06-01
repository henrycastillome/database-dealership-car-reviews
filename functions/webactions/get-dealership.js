/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
require('dotenv').config();

const params={
    IAM_API_KEY: process.env.IAM_API_KEY,
    COUCH_URL: process.env.COUCH_URL
}


async function main() {
    try{
       const validAccess= await authentication(params);
       let dbDetails= await validAccess.postAllDocs({db:'dealerships',limit:20, includeDocs:true})
       return {"body": dbDetails.result.rows }
       
   } catch(error){
       return {body:{error:error.description}}
   }
}

function authentication(params){
  const authenticator= new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant= CloudantV1.newInstance({
      authenticator:authenticator
  })
  cloudant.setServiceUrl(params.COUCH_URL);

 
  return cloudant;
}

// get dealership by state
async function main(st) {
  try{
     const validAccess= await authentication(param);
    
     const selector={state:st.state}
    
     let dbDetails= await validAccess.postFind({db:'dealerships',selector:selector})
     return {"body": dbDetails.result.docs }
     
 } catch(error){
     return {body:{error:error.description}}
 }
}

function authentication(params){
const authenticator= new IamAuthenticator({ apikey: params.IAM_API_KEY })
const cloudant= CloudantV1.newInstance({
    authenticator:authenticator
})
cloudant.setServiceUrl(params.COUCH_URL);


return cloudant;
}



//get dealership by id

async function main(st) {
    try{
       const validAccess= await authentication(param);
       const id= parseInt(st.id)
      
       const selector={id:id}
      
       let dbDetails= await validAccess.postFind({db:'dealerships',selector:selector})
       return {"body": dbDetails.result.docs }
       
   } catch(error){
       return {body:{error:error.description}}
   }
}

function authentication(params){
  const authenticator= new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant= CloudantV1.newInstance({
      authenticator:authenticator
  })
  cloudant.setServiceUrl(params.COUCH_URL);

 
  return cloudant;
}