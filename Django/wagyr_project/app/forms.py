from django import forms
from app.models import dailySched

class dailySchedForm(forms.ModelForm):
    month = forms.IntegerField(help_text="Enter a month.")
    day = forms.IntegerField(help_text="Enter a day.")

    class Meta:
        model = dailySched
        fields = ('month', 'day')