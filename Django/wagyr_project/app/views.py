from django.shortcuts import render, redirect
from app.forms import searchGamebyTeam, createWagyrbyGame, LoginForm, UserCreateForm, StripeForm, \
    CrispyPasswordChangeForm
from app.models import Game, Team
from django.db.models import Q
from app.services import api_query_sched, check_sched_loaded
from app.services_post import api_query_sched as aqs_post, check_sched_loaded as csl_post
import time
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
import stripe
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone


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


class PasswordChange(LoginRequiredMixin, TemplateView):
    template_name = 'bootstrap/password_change_form.html'

    def get(self, request, *args, **kwargs):
        password_change_form = CrispyPasswordChangeForm(request.user)
        return render(request, self.template_name, {'password_change_form': password_change_form})

    def post(self, request):
        form = CrispyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/password_change/done/')
        else:
            return render(request, self.template_name, {'password_change_form': form})


@login_required()
def password_change_done(request):
    return render(request, 'bootstrap/password_change_done.html')


# Stripe Payments
#####################################################
class StripeMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = "pk_test_GQYJHTl83M2zVUICU8unRENH"  # change to live publishable key
        return context


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'bootstrap/payment_successful.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PaymentView(LoginRequiredMixin, StripeMixin, FormView):
    # Wagyr loser does this
    template_name = 'bootstrap/payment.html'
    form_class = StripeForm
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        stripe.api_key = "sk_test_ikub1dIq78V4qb52oTTAsYat"  # change to live secret key

        token = self.request.POST['stripe_token']

        try:
            stripe.Charge.create(
                amount=1000,  # amount in cents
                currency="usd",
                source=token,
                description="Wagyr Charge"
            )
            return super(PaymentView, self).form_valid(form)
        except stripe.error.CardError as e:
            # The card has been declined
            print(e)
            pass


class Received_SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'bootstrap/received_payment_successful.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ReceivePaymentView(LoginRequiredMixin, StripeMixin, FormView):
    # Wagyr winner does this
    template_name = 'bootstrap/receive_payment.html'  # it's the same form for making a payment!
    form_class = StripeForm
    success_url = reverse_lazy('received_thank_you')

    def form_valid(self, form):
        stripe.api_key = "sk_test_ikub1dIq78V4qb52oTTAsYat"  # change to live secret key

        token = self.request.POST['stripe_token']
        # TODO Get user from the wagyr
        recipient = stripe.Recipient.create(
            name="John Doe",  # str(User.first_name) + str(User.last_name)
            type="individual",
            email="payee@example.com",  # str(User_email)
            card=token
        )
        transfer = stripe.Transfer.create(
            amount=1000,
            currency="usd",
            recipient=recipient.id,
            statement_descriptor="WAGYR",
        )
        return super(ReceivePaymentView, self).form_valid(form)


# HTML Views
#########################################################
@login_required(login_url='/welcome', redirect_field_name='')
def index(request):
    games = Game.objects.filter(date__lte=timezone.now() + timezone.timedelta(days=1),
                                date__gt=timezone.now() - timezone.timedelta(days=20))
    form = searchGamebyTeam()
    return render(request, 'bootstrap/index.html', {'games': games, 'search_form': form})


def welcome(request):
    games = Game.objects.filter(date__lte=timezone.now() + timezone.timedelta(days=1),
                                date__gt=timezone.now() - timezone.timedelta(days=20))
    return render(request, 'bootstrap/welcome.html', {'games': games})


def about(request):
    return render(request, 'bootstrap/about.html')


def contact(request):
    return render(request, 'bootstrap/contact.html')


@login_required()
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'bootstrap/profile.html', {'user': user})


@login_required()
def wagyrs(request):
    return render(request, 'bootstrap/wagyr.html')


class MakeWagyr(TemplateView):
    def get(self, request, *args, **kwargs):
        game_id = request.GET['game_id']
        obj = Game.objects.get(pk=game_id)
        split = obj.home_team.name.split(' ')
        if len(split) > 2:
            homeLocation = split[0] + ' ' + split[1]
            homeTeam = split[2]
        else:
            homeLocation = split[0]
            homeTeam = split[1]
        split = obj.away_team.name.split(' ')
        if len(split) > 2:
            awayLocation = split[0] + ' ' + split[1]
            awayTeam = split[2]
        else:
            awayLocation = split[0]
            awayTeam = split[1]
        form = createWagyrbyGame()
        return render(request, 'bootstrap/make_wagyr.html',
                      {'create_wagyr_form': form, 'game': obj, 'homeLocation': homeLocation,
                       'awayLocation': awayLocation, 'homeTeam': homeTeam, 'awayTeam': awayTeam})

    def post(self, request):
        username = request.user.username
        game_id = request.POST.get('game_id')
        form = createWagyrbyGame(request.POST, initial={'self_id': username, 'game_id': game_id, 'wagyr_id': 0})
        if form.is_valid():
            form.save(request)
            return render(request, 'bootstrap/index.html')
        else:
            print(form.errors)
            return render(request, 'bootstrap/index.html')


@login_required()
def searchByTeam(request):
    form = searchGamebyTeam()
    return render(request, 'bootstrap/team_schedule.html', {'search_form': form})


@login_required()
def search_reg(request):
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


def search_post(request):
    start = time.time()

    search_term = request.POST['team'].title()

    messages = []
    err = []
    messages.append("Querying internal DB for Playoff Games that the " + str(search_term) + " are playing in")

    games = Game.objects.select_related('home_team', 'away_team').filter(
        Q(away_team__name__contains=search_term) | Q(home_team__name__contains=search_term))

    if not games:
        api_query = aqs_post(search_term, messages, err)

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
        csl_post(games[0].get_search_team(search_term), messages, err)
        messages.append("Found " + str(games.count()) + " in our database")
        end = time.time()
        messages.append("Time elapsed = " + str(end - start) + " seconds")
        return render(request, 'bootstrap/results.html', {'games': games, 'debug': messages, 'errors': len(err)})