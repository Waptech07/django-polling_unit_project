from django import forms
from .models import LGA
from .models import PollingUnit
from .models import Party

class LocalGovernmentForm(forms.Form):
    lga = forms.ModelChoiceField(queryset=LGA.objects.all(), empty_label="Select a Local Government")


class PollingUnitResultForm(forms.ModelForm):
    class Meta:
        model = PollingUnit
        fields = ['name', 'ward']  # Add any other relevant fields from the PollingUnit model

    def __init__(self, *args, **kwargs):
        super(PollingUnitResultForm, self).__init__(*args, **kwargs)

        # Dynamically add fields for each party's result
        parties = Party.objects.all()
        for party in parties:
            field_name = f'party_{party.id}'
            self.fields[field_name] = forms.IntegerField(label=party.name)
