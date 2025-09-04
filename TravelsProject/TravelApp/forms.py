from django import forms

import TravelApp
from .models import *

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['destination', 'price', 'duration', 'image']

    def __init__(self, *args, **kwargs):
        super(TravelForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'image':
                visible.field.widget.attrs['class'] = 'form-control'