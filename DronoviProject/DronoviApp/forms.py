from django import forms
import DronoviApp
from .models import *

class RezervacijaForm(forms.ModelForm):
    class Meta:
        model = Rezervacija
        fields = '__all__'
        exclude = ('odgovoren',)

    def __init__(self, *args, **kwargs):
        super(RezervacijaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'