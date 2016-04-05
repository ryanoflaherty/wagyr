from django.shortcuts import render_to_response, render
from app.forms import searchGamebyTeam
from app.models import Game
import requests
from django.http import HttpResponse, JsonResponse
import datetime

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
	response = []

	if request.GET["team"] != None:
		for g in data["games"]:
			if g["away"]["name"] == request.GET['team'] or g["home"]["name"] == request.GET['team']:
				if g["status"] != "closed":
					data = {}
					data["event_id"] = g["id"]
					data["date"] = g["scheduled"]
					data["status"] = g["status"]
					data["venue_id"] = g["venue"]["id"]
					data["away_id"] = g["away"]["id"]
					data["away_team"] = g["away"]["name"]
					data["home_id"] = g["home"]["id"]
					data["home_team"] = g["home"]["name"]
					response.append(data)

		return render(request, 'bootstrap/results.html', {'response': response})
	else:
		return HttpResponse('404 Error')

def searchByTeam(request):
	form = searchGamebyTeam()
	return render(request, 'bootstrap/team_schedule.html', {'form': form})