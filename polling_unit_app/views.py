from django import forms
from django.shortcuts import redirect, render
from polling_unit_app.forms import PollingUnitResultForm
from .models import AnnouncedPUResult, Party, PollingUnit, LGA
from polling_unit_app import models
from polling_unit_app.models import State

# Create your views here.

def polling_unit_results(request, polling_unit_id):
    try:
        polling_unit = PollingUnit.objects.get(pk=polling_unit_id)
        results = AnnouncedPUResult.objects.filter(polling_unit=polling_unit)
        return render(request, 'polling_unit_results.html', {'polling_unit': polling_unit, 'results': results})
    except PollingUnit.DoesNotExist:
        # Handle the case where the polling unit doesn't exist
        return render(request, 'polling_unit_not_found.html')

def calculate_total_result(lga_id):
    lga = LGA.objects.get(pk=lga_id)
    polling_units = PollingUnit.objects.filter(ward__lga=lga)
    total_result = AnnouncedPUResult.objects.filter(polling_unit__in=polling_units).aggregate(total=models.Sum('result'))['total']
    return total_result or 0

def local_government_results(request):
    lgas = LGA.objects.all()
    selected_lga_id = request.GET.get('lga', None)
    total_result = 0

    if selected_lga_id:
        total_result = calculate_total_result(selected_lga_id)

    return render(request, 'local_government_results.html', {'lgas': lgas, 'selected_lga_id': selected_lga_id, 'total_result': total_result})

def add_polling_unit_result(request):
    if request.method == 'POST':
        form = PollingUnitResultForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new polling unit result
            form.save()
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = PollingUnitResultForm()
    
    return render(request, 'add_polling_unit_result.html', {'form': form})

class PollingUnitResultForm(forms.ModelForm):
    class Meta:
        model = PollingUnit
        fields = ['name', 'ward']  # Add any other relevant fields from the PollingUnit model

    # Create fields for each party's result
    parties = Party.objects.all()
    for party in parties:
        field_name = f'party_{party.id}'
        forms.Field[field_name] = forms.IntegerField(label=party.name)