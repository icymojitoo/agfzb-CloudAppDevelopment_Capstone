const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

require('dotenv').config();
 
async function main() {
     
    const authenticator = new IamAuthenticator({ apikey: process.env.API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(process.env.COUCH_URL);

    const review_inputs = {
    id: params['review']['id'],
    name: params['review']['name'],
    dealership: params['review']['dealership'],
    review: params['review']['review'],
    purchase: params['review']['purchase'],
    another: params['review']['another'],
    purchase_date: params['review']['purchase_date'],
    car_make: params['review']['car_make'],
    car_model: params['review']['car_model'],
    car_year: params['review']['car_year'],
    };

    try {
        cloudant.postDocument({
            db: 'reviews',
            document: review_inputs
            }).then(response => {
            return {
                statusCode: 200,
            }
            })
            .catch(err => {
                console.log(err);
            }
        );


    } catch (err) {
        console.log(err);
        if (err.statusCode === 500) {
            return {
                statusCode: 500,
                body: 'Something went wrong on the server'
            }
        }
        else {
            return {
                statusCode: err.statusCode,
                body: err.message
            }
        }
    }
}

// /api/review
