from django.urls import path
from .views import aircraft_search_view

app_name = 'aviapage_search' # set the app name as the namespace
urlpatterns = [
    path('', aircraft_search_view, name='aircraft_search'),
    
]
