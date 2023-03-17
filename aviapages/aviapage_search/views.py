
import requests, os
from django.shortcuts import render
from .forms import AircraftSearchForm
from .utils import get_aircraft_list

def aircraft_search_view(request):
    aircraft_list = get_aircraft_list()
    if aircraft_list is None:
        aircraft_list = []

    if request.method == 'POST':
        form = AircraftSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            filtered_list = [aircraft for aircraft in aircraft_list if 
                 (aircraft.get('tail_number') is not None and aircraft.get('tail_number').startswith(search_query)) or 
                 (aircraft.get('serial_number') is not None and aircraft.get('serial_number').startswith(search_query))]

            for aircraft in filtered_list:
                images = aircraft.get('images', [])
                if images is not None:
                    aircraft['image_urls'] = [image['url'] for image in images[:3]]

            # Select only the desired fields for each aircraft
            filtered_list = [{ 'home_base': aircraft['home_base'],'company_name':aircraft['company_name'],'tail_number': aircraft['tail_number'], 'serial_number': aircraft['serial_number'], 'aircraft_type_name': aircraft['aircraft_type_name'], 'year_of_production': aircraft['year_of_production'], 'image_urls': aircraft.get('image_urls', []) } for aircraft in filtered_list]

            # Limit the number of results displayed to a maximum of 300
            filtered_list = filtered_list[:300]
            
            # Pass the list of filtered aircraft to the template
            context = {'aircraft_list': filtered_list, 'form': form}
            return render(request, 'aircraft_search_results.html', context=context)
    else:
        form = AircraftSearchForm()

    context = {'form': form}
    return render(request, 'aircraft_search.html', context=context)



def aircraft_details_view(request, tail_number, company_name=None):
    aircraft_url = f'https://dir.aviapages.com/api/aircraft/?ordering=aircraft_id&search_tail_number={tail_number}'
    print(aircraft_url)
    company_url = f'https://dir.aviapages.com/api/companies/?ordering=company_id&search_name={company_name}'
    print(company_url)
    api_token = os.getenv('API_KEY')
    headers = {'Authorization': api_token}
    params = {'features': True, 'images': True}

    aircraft_response = requests.get(aircraft_url, headers=headers, params=params)
    company_response = requests.get(company_url, headers=headers)

    if aircraft_response.status_code == 200 and company_response.status_code == 200:
        aircraft_list = aircraft_response.json()['results']
        company_list = company_response.json()['results']
        
        if aircraft_list:
            aircraft = aircraft_list[0]
            images = aircraft.get('images', [])
            home_base = aircraft.get('home_base')
            
            if home_base:
                print('yes')
                airport_url = f"https://dir.aviapages.com/api/airports/?on_date=2025-02-20T01%3A00&ordering=airport_id&search_icao={home_base}"
                airport_response = requests.get(airport_url, headers=headers)
                print(airport_response.content)
                if airport_response.status_code == 200:
                    airport_list = airport_response.json()['results']
                    
                    if airport_list:
                        airport = airport_list[0]
                        context = {'aircraft': aircraft, 'company': company_list[0], 'airport': airport}
                    else:
                        context = {'aircraft': aircraft, 'company': company_list[0], 'error': 'Failed to retrieve airport details.'}
                else:
                    context = {'aircraft': aircraft, 'company': company_list[0], 'error': 'Failed to retrieve airport details.'}
            else:
                context = {'aircraft': aircraft, 'company': company_list[0], 'error': 'Failed to retrieve airport details.'}
        else:
            context = {'error': 'Failed to retrieve aircraft details.'}

        return render(request, 'aircraft_details.html', context=context)
    else:
        print("Failed to retrieve aircraft details. Status code:", aircraft_response.status_code)
        return render(request, 'aircraft_details.html', {'error': 'Failed to retrieve aircraft details.'})



