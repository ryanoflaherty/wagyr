from django.shortcuts import render_to_response, render
from app.forms import dailySchedForm
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


def daily_sched(request):
	if request.method == 'POST':
		form = dailySchedForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)

			day = form.cleaned_data['day']
			month = form.cleaned_data['month']

			url = "http://api.sportradar.us/ncaamb-t3/games/2016/"
			url += str(month)
			url += "//"
			url += str(day)
			url += "//"
			url += "schedule.json"

			# Now call the index() view.
			# The user will be shown the homepage.
			params = {'api_key': 'ukhq6uys9ukzy4rg9p8y5ejw'}
			response = requests.get(url, params)
			data = response.json()
			games_dict = {'games': data['games']}
			return JsonResponse(games_dict)
			#return render(request, 'bootstrap/test.html', games_dict)
		else:
			return render_to_response('bootstrap/index.html')

	else:
		# If the request was not a POST, display the form to enter details.
		form = dailySchedForm()

		# Bad form (or form details), no form supplied...
		# Render the form with error messages (if any).
		return render(request, 'bootstrap/daily_sched.html', {'form': form})

def test(request):
		return render_to_response('bootstrap/test.html')