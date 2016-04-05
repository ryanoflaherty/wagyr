from django.shortcuts import render_to_response, render
from app.forms import searchGamebyTeam
from app.models import Game
import requests
from django.http import HttpResponse, JsonResponse

def index(request):
		return render_to_response('bootstrap/index.html')


def about(request):
		return render_to_response('bootstrap/about.html')


def services(request):
		return render_to_response('bootstrap/services.html')


def contact(request):
		return render_to_response('bootstrap/contact.html')



"""
url = "http://api.sportradar.us/ncaamb-t3/games/2016/"
url += str(month)
url += "//"
url += str(day)
url += "//"
url += "schedule.json"

# Now call the index() view.
# The user will be shown the homepage.
#
data = response.json()
games_dict = {'games': data['games']}
"""


def search(request):

	url = "http://api.sportradar.us/nba-t3/games/2015/REG/schedule.json"
	params = {'api_key': 'wfejyy6af8z84n9u8rdhrcgj'}
	api_response = requests.get(url, params)
	data = api_response.json()
	#schedule_dict =

	if 'team' in request.GET:
		response = 'You searched for: %r' % request.GET['team']
	else:
		response = 'You submitted an empty form.'
	return render(request, 'bootstrap/results.html', {'response': data})

def searchByTeam(request):
	form = searchGamebyTeam()
	return render(request, 'bootstrap/team_schedule.html', {'form': form})