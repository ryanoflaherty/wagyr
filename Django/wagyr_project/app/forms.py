from django import forms
from app.models import dailySched, Game

class dailySchedForm(forms.ModelForm):
    month = forms.CharField()
    day = forms.CharField()

    class Meta:
        model = dailySched
        fields = ('month', 'day')


class searchGamebyTeam(forms.ModelForm):
    team = forms.CharField()

    class Meta:
        model = Game
        fields = ('team',)