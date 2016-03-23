from django import forms
from app.models import dailySched

class dailySchedForm(forms.ModelForm):
    month = forms.CharField()
    day = forms.CharField()

    class Meta:
        model = dailySched
        fields = ('month', 'day')