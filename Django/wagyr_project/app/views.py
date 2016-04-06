from django.shortcuts import render_to_response, render
from app.forms import searchGamebyTeam
from app.models import Game
from django.shortcuts import get_list_or_404
from django.db.models import Q
from app.services import query_api_sched
import time
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


def searchByTeam(request):
    form = searchGamebyTeam()
    return render(request, 'bootstrap/team_schedule.html', {'form': form})


def search(request):
    start = time.time()
    search_term = request.GET['team']
    messages = []
    messages.append("Querying internal DB for Games that the " + str(search_term) + " are playing in")

    games = Game.objects.filter(Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))

    if not games:
        messages.append("No games found in our database, querying API")
        api_query = query_api_sched(search_term, messages)
        if api_query:
            messages.append("Found " + str(api_query) + " results for future games")
            games = Game.objects.filter(Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))
            end = time.time()
            messages.append("Time elapsed = " + str(end - start) + " seconds")
            return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages})
        else:
            messages.append("Could not query API or no search query provided")
            end = time.time()
            messages.append("Time elapsed = " + str(end - start) + " seconds")
            return render(request, 'bootstrap/results.html', {'debug': messages})
    else:
        messages.append("Found " + str(len(games)) + " in our database")
        end = time.time()
        messages.append("Time elapsed = " + str(end-start) + " seconds")
        return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages})


