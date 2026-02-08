import requests
from requests_oauthlib import OAuth1

# Replace with your FatSecret API keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

BASE_URL = 'https://platform.fatsecret.com/rest/server.api'

# OAuth1 for FatSecret
oauth = OAuth1(client_key=CONSUMER_KEY,
               client_secret=CONSUMER_SECRET,
               signature_method='HMAC-SHA1')

def search_food(query):
    params = {
        'method': 'foods.search',
        'search_expression': query,
        'format': 'json'
    }
    response = requests.get(BASE_URL, params=params, auth=oauth)
    data = response.json()
    foods = data.get('foods', {}).get('food', [])
    
    # If only one food is returned, wrap it in a list
    if isinstance(foods, dict):
        foods = [foods]
    return foods

def get_food_details(food_id):
    """Get detailed food info including calories and macros"""
    params = {
        'method': 'food.get',
        'food_id': food_id,
        'format': 'json'
    }
    response = requests.get(BASE_URL, params=params, auth=oauth)
    data = response.json()
    return data.get('food', {})
