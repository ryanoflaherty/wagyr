from django.shortcuts import render, redirect
from app.forms import searchGamebyTeam, createWagyrbyGame, LoginForm, UserCreateForm
from app.models import Game, Team
from django.db.models import Q
from app.services import api_query_sched, get_create_team, check_sched_loaded
import time
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


# User Login and Register
###################################################################
class Login(TemplateView):
    template_name = 'bootstrap/login.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            login_form = LoginForm()
            return render(request, self.template_name, {'login_form': login_form})
        else:
            return redirect('index')

    def post(self, request):
        form = LoginForm(None, request.POST or None)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect('index', permanent=True)
        else:
            return render(request, self.template_name, {'login_form': form})


@login_required()
def logout(request):
    template_name = 'bootstrap/logout.html'
    logout_user(request)
    return render(request, template_name)


class CreateUser(TemplateView):
    template_name = 'bootstrap/registration_form.html'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, self.template_name, {'user_create_form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            request.session["temp_user"] = {
                'username': username,
                'new': True,
            }
            return redirect('/accounts/register/done/')
        else:
            return render(request, self.template_name, {'user_create_form': form})


def user_create_done(request):
    new_user = request.session["temp_user"]["username"]
    is_new = request.session["temp_user"]["new"]

    if new_user:
        request.session["temp_user"] = ""
        user = User.objects.get(username=new_user)
        return render(request, 'bootstrap/registration_complete.html', {'new_user': user, 'is_new': is_new})
    else:
        return redirect('/accounts/login/')


def index(request):
    return render(request, 'bootstrap/index.html')


def about(request):
    return render(request, 'bootstrap/about.html')


def contact(request):
    return render(request, 'bootstrap/contact.html')


@login_required()
def profile(request):
    return render(request, 'bootstrap/profile.html')


@login_required()
def wagyrs(request):
    return render(request, 'bootstrap/wagyr.html')


class MakeWagyr(TemplateView):
    def get(self, request, *args, **kwargs):
        game_id = request.GET['game_id']
        obj = Game.objects.get(pk=game_id)
        form = createWagyrbyGame()
        return render(request, 'bootstrap/make_wagyr.html', {'create_wagyr_form': form, 'game': obj})


# @login_required()
def searchByTeam(request):
    form = searchGamebyTeam()
    return render(request, 'bootstrap/team_schedule.html', {'search_form': form})


# @login_required()
def search(request):
    start = time.time()
    search_term = request.POST['team'].title()

    messages = []
    err = []
    messages.append("Querying internal DB for Games that the " + str(search_term) + " are playing in")

    # TODO (Ryan) If we add one teams whole schedule, this query will return true for a couple games for every team.
    # need a way to validate that the whole schedule is there

    # FIXED Created an instance method to check if the schedule is loaded

    # Check to see if the team you are searching for has any games, preload team objects if it is found
    games = Game.objects.select_related('home_team', 'away_team').filter(
        Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))

    if not games:
        api_query = api_query_sched(search_term, messages, err)

        if api_query:
            messages.append("Found " + str(api_query) + " results for future games")
            games = Game.objects.filter(
                Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))
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
        messages.append("Time elapsed = " + str(end - start) + " seconds")
        return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages, 'errors': len(err)})
