
import requests
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
            filtered_list = [{ 'tail_number': aircraft['tail_number'], 'serial_number': aircraft['serial_number'], 'aircraft_type_name': aircraft['aircraft_type_name'], 'year_of_production': aircraft['year_of_production'], 'image_urls': aircraft.get('image_urls', []) } for aircraft in filtered_list]

            # Limit the number of results displayed to a maximum of 300
            filtered_list = filtered_list[:300]
            
            # Pass the list of filtered aircraft to the template
            context = {'aircraft_list': filtered_list, 'form': form}
            return render(request, 'aircraft_search_results.html', context=context)
    else:
        form = AircraftSearchForm()

    context = {'form': form}
    return render(request, 'aircraft_search.html', context=context)


def aircraft_details_view(request, tail_number):
    url = f'https://dir.aviapages.com/api/aircraft/?ordering=aircraft_id&search_tail_number={tail_number}'
    print(url)
    headers = {'Authorization': 'Token BN442rPF4zTfWAGQDqrZgjRWKznDfxUg9VK'}
    params = {'features': True, 'images': True}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        aircraft = response.json()['results']
        #print("aircraft", aircraft)

        #images = aircraft.get('images', [])
        #aircraft['image_urls'] = [image['url'] for image in images[:3]]
        
        context = {'aircraft': aircraft}
        
        return render(request, 'aircraft_details.html', context=context)
    else:
        print("Failed to retrieve aircraft details. Status code:", response.status_code)
        return render(request, 'aircraft_details.html', {'error': 'Failed to retrieve aircraft details.'})