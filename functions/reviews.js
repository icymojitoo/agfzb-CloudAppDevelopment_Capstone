const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
require('dotenv').config();
 
async function main() {
     
    const authenticator = new IamAuthenticator({ apikey: process.env.API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(process.env.COUCH_URL);
    try {
    let dbList = await cloudant.postAllDocs({
        db: 'reviews',
        includeDocs: true
    });

    reviews = []
    for (let i = 0; i < dbList.result.rows.length; i++) {
        if (dbList.result.rows[i].doc.dealership == params['dealerId']) {
        reviews.push(dbList.result.rows[i].doc);
        }
    }
    return { "dbs": reviews };
    } 
    catch (err) {
        console.log(err);
        if (err.statusCode === 404) {
            return {
                statusCode: 404,
                body: 'The state does not exist'
            }
        } else if (err.statusCode === 500) {
            return {
                statusCode: 500,
                body: 'Something went wrong on the server'
            }
        } else {
            return {
                statusCode: err.statusCode,
                body: err.message
            }
        }
    }
}


// /api/review?dealerId=""