import requests

def get_aircraft_list():
    url = 'https://dir.aviapages.com/api/aircraft/'
    headers = {'Authorization': 'Token BN442rPF4zTfWAGQDqrZgjRWKznDfxUg9VK'}
    params = {'features': True, 'images': True}
    response = requests.get(url, headers=headers, params=params)
    #print("=====================",response.content)
    if response.status_code == 200:
        aircraft_list = response.json()['results']
        print("Aircraft list retrieved successfully.")
        #print(aircraft_list)
        return aircraft_list
    else:
        print("Failed to retrieve aircraft list. Status code:", response.status_code)
        return None