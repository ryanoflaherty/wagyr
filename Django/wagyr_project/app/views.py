from django.shortcuts import render
from app.forms import searchGamebyTeam
from app.models import Game, Team
from django.db.models import Q
from app.services import api_query_sched, get_create_team, check_sched_loaded
import time
import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'bootstrap/index.html')


def about(request):
    return render(request, 'bootstrap/about.html')


def services(request):
    return render(request, 'bootstrap/services.html')


def contact(request):
    return render(request, 'bootstrap/contact.html')


@login_required()
def profile(request):
    return render(request, 'bootstrap/profile.html')


@login_required()
def wagyrs(request):
    return render(request, 'bootstrap/wagyr.html')


@login_required()
def searchByTeam(request):
    form = searchGamebyTeam()
    return render(request, 'bootstrap/team_schedule.html', {'form': form})


@login_required()
def search(request):
    start = time.time()

    search_term = request.GET['team'].title()

    messages = []
    err = []
    messages.append("Querying internal DB for Games that the " + str(search_term) + " are playing in")

    # TODO (Ryan) If we add one teams whole schedule, this query will return true for a couple games for every team.
    # need a way to validate that the whole schedule is there

    # FIXED Created an instance method to check if the schedule is loaded

    # Check to see if the team you are searching for has any games, preload team objects if it is found
    games = Game.objects.select_related('home_team', 'away_team').filter(Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))

    if not games:
        api_query = api_query_sched(search_term, messages, err)

        if api_query:
            messages.append("Found " + str(api_query) + " results for future games")
            games = Game.objects.filter(Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))
            end = time.time()
            messages.append("Time elapsed = " + str(end - start) + " seconds")
            return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages, 'errors': len(err)})

        else:
            messages.append("Error getting schedule")
            end = time.time()
            messages.append("Time elapsed = " + str(end - start) + " seconds")
            return render(request, 'bootstrap/results.html', {'debug': messages, 'errors': len(err)})
    else:
        check_sched_loaded(games[0].get_search_team(search_term), messages, err)
        messages.append("Found " + str(games.count()) + " in our database")
        end = time.time()
        messages.append("Time elapsed = " + str(end-start) + " seconds")
        return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages, 'errors': len(err)})


