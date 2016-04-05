from django import forms
from app.models import Game


class searchGamebyTeam(forms.ModelForm):
    team = forms.CharField(label='team', max_length=100)

    class Meta:
        model = Game
        fields = ('team',)