from django import forms
import NedvizninaApp
from .models import *


class RealEstateForm(forms.ModelForm):
    class Meta:
        model = RealEstate
        fields = ['name', 'description', 'area', 'date_published', 'photo', 'isReserved', 'isSold']

    def __init__(self, *args, **kwargs):
        super(RealEstateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(field_name)
            if field_name not in ["isReserved", "isSold"]:
                field.widget.attrs['class'] = 'form-control'