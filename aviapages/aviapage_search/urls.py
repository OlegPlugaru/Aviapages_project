from django.urls import path
from .views import aircraft_search_view,aircraft_details_view

app_name = 'aviapage_search' # set the app name as the namespace
urlpatterns = [
    path('', aircraft_search_view, name='aircraft_search'),
     # new URL pattern for aircraft details
    path('aircraft/<str:tail_number>/details/', aircraft_details_view, name='aircraft_details'),
]