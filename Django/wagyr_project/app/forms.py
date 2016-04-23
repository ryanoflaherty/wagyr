from django import forms
from app.models import Game


class searchGamebyTeam(forms.ModelForm):
	team = forms.CharField(label='Search for your favorite team', max_length=100)

	class Meta:
		model = Game
		fields = ('team',)

class createWagyrbyGame(forms.ModelForm):
	class Meta:
		model = Game
		fields = ('event_id',)




