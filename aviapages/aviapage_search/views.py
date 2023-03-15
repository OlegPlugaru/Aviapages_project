import requests
from django.shortcuts import render, get_object_or_404
from .forms import AircraftSearchForm
from .utils import get_aircraft_list
from .models import Aircraft

def aircraft_search_view(request):
    aircraft_list = get_aircraft_list()
    if aircraft_list is None:
        aircraft_list = []

    if request.method == 'POST':
        form = AircraftSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            print(search_query)
            filtered_list = [aircraft for aircraft in aircraft_list if 
                 (aircraft.get('tail_number') is not None and aircraft.get('tail_number').startswith(search_query)) or 
                 (aircraft.get('serial_number') is not None and aircraft.get('serial_number').startswith(search_query))]

            for aircraft in filtered_list:
                images = aircraft.get('images', [])
                if images is not None:
                    aircraft['image_urls'] = [image['url'] for image in images[:3]]

            # Add aircraft_id to the context
            context = {'aircraft_list': filtered_list, 'form': form}
            if filtered_list:
                context['aircraft_id'] = filtered_list[0].get('aircraft_id')
                print(context['aircraft_id'])
            else:
                context['aircraft_id'] = None

            # Limit the number of results displayed to a maximum of 300
            filtered_list = filtered_list[:300]        
            
            return render(request, 'aircraft_search_results.html', context=context)
    else:
        form = AircraftSearchForm()

    context = {'aircraft_list': aircraft_list, 'form': form}
    return render(request, 'aircraft_search.html', context=context)


