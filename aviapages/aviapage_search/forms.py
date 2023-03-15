from django import forms

class AircraftSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=True, label='Serial or tail number')