from django import forms
from.models import Survey

class DateInput(forms.DateInput):
    input_type = 'date'

class EditSurveyInfoForm(forms.ModelForm):
    class Meta:
        widgets = {'expiry_date': DateInput()}
        model = Survey
        fields = ["name", "expiry_date"]