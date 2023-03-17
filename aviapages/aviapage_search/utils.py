import requests
import os 

def get_aircraft_list():
    url = 'https://dir.aviapages.com/api/aircraft/'
    api_token = os.getenv('API_KEY')
    headers = {'Authorization': api_token}
    params = {'features': True, 'images': True}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        aircraft_list = response.json()['results']
        print("Aircraft list retrieved successfully.")
        return aircraft_list
    else:
        print("Failed to retrieve aircraft list. Status code:", response.status_code)
        return None