from django.urls import path
from .views import aircraft_search_view,aircraft_details_view

app_name = 'aviapage_search' 
urlpatterns = [
    path('', aircraft_search_view, name='aircraft_search'),
    path('aircraft/<str:tail_number>/<str:company_name>/details/', aircraft_details_view, name='aircraft_details'),
]