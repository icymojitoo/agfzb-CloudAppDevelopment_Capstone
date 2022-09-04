from cProfile import label
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from django.conf import settings


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)

    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['dbs']
        for i in range(len(dealers)):
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealers[i]["address"],
                city=dealers[i]["city"], 
                full_name=dealers[i]["full_name"],
                id=dealers[i]["id"],
                lat=dealers[i]["lat"],
                long=dealers[i]["long"],
                short_name=dealers[i]["short_name"],
                st=dealers[i]["st"],
                zip=dealers[i]["zip"]
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    results = []
    print('a')
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result['dbs']
        for i in range(len(reviews)):
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                car_make=reviews[i]["car_make"],
                car_model=reviews[i]["car_model"],
                car_year=reviews[i]["car_year"],
                dealership=reviews[i]["dealership"],
                name=reviews[i]["name"], 
                purchase=reviews[i]["purchase"],
                purchase_date=reviews[i]["purchase_date"],
                review=reviews[i]["review"],
                id=reviews[i]["id"],
                sentiment = analyze_review_sentiments(reviews[i]["review"]),
            )
            results.append(review_obj)
        print('b')
        return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

    # Create an authenticator
    authenticator = IAMAuthenticator(settings.WATSON_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(settings.WATSON_API_URL)

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,)
        )).get_result()

    sentiment = response['keywords'][0]['sentiment']['label']
    return sentiment

def post_request(url, json_payload, **kwargs):
    req = requests.post(url, params=kwargs, json=json_payload)

