import requests
from app.models import Game, Venue, Team, Wagyr
import time
from django.core.cache import cache
from django.utils import timezone


def check_sched_loaded(Team, messages, err):
    print("check_sched")
    messages.append("Checking to see if schedule is loaded for " + Team.name)

    if not Team.is_pst_sched_loaded():
        messages.append("Schedule not loaded, getting it now")
        count = get_games(Team, messages, err)
        if count:
            return count
    else:
        messages.append("Schedule is already loaded")


def api_query_sched(search_term, messages, err):
    print("api_query")
    messages.append("No games found in our database, querying API for Team data")
    newTeam, created = get_create_team(search_term, messages, err)

    if newTeam:
        if created:
            messages.append("New entry for " + newTeam.name + " successful, getting schedule")
            count = get_games(newTeam, messages, err)
            return count
        else:
            count = check_sched_loaded(newTeam, messages, err)
            return count
    else:
        return None


def get_games(Team, messages, err):
    print("get_games")

    # Use fast cache if it exists
    data = cache.get('schedule')
    if not data:
        schedule_url = "http://api.sportradar.us/nba-t3/games/2015/PST/schedule.json"
        params = {'api_key': 'pa8j2hgacuvgkavsz5zfna7n'}
        try:
            schedule_response = requests.get(schedule_url, params)
            data = schedule_response.json()
            messages.append("Received data from API")
            cache.set('schedule', data)
            messages.append("Set cache")
        except ValueError as e:
            print(e)
            err.append(e)
            time.sleep(1)
            schedule_response = requests.get(schedule_url, params)
            data = schedule_response.json()
            messages.append("Received data from API")
            messages.append("Set cache")
            pass
    else:
        messages.append("Using cached data")

    count = 0

    for g in data["games"]:
        if Team.name in g["away"]["name"] or Team.name in g["home"]["name"]:
            if g["status"]: #!= "closed":
                count += 1

                # Check for non US
                if not g["venue"]["country"] == 'USA':
                    g["venue"]["zip"] = ''
                    g["venue"]["state"] = ''

                # Save Venue first if it does not exist due to Foreign key constraint
                venue, created = Venue.objects.get_or_create(
                    pk=g["venue"]["id"],
                    defaults={
                        'name': g["venue"]["name"],
                        'capacity': int(g["venue"]["capacity"]),
                        'city': g["venue"]["city"],
                        'zip': g["venue"]["zip"],
                        'country': g["venue"]["country"],
                        'state': g["venue"]["state"],
                        'address': g["venue"]["address"],
                    }
                )

                if created:
                    messages.append("Created venue " + venue.name)
                else:
                    messages.append("Venue exists")

                if Team.name == g["home"]["name"]:
                    # Check away team to see if it is in the DB. If not, create it
                    opponent, new = get_create_team(g["away"]["name"], messages, err)

                    # Create game instance
                    game, created = Game.objects.get_or_create(
                        pk=g["id"],
                        defaults={
                            'date': g["scheduled"],
                            'status': g["status"],
                            'venue': venue,
                            'away_team': opponent,
                            'home_team': Team,
                        }
                    )
                    if created:
                        messages.append("Adding new game to the database... " + g["home"]["name"] + " vs " + g["away"]["name"])
                else:
                    # Check away team to see if it is in the DB. If not, create it
                    opponent, new = get_create_team(g["home"]["name"], messages, err)

                    # Create game instance
                    game, created = Game.objects.get_or_create(
                        pk=g["id"],
                        defaults={
                            'date': g["scheduled"],
                            'status': g["status"],
                            'venue': venue,
                            'away_team': Team,
                            'home_team': opponent,
                        }
                    )
                    if created:
                        messages.append("Adding new game to the database... " + g["home"]["name"] + " @ " + g["away"]["name"])
    return count


def get_create_team(search_term, messages, err):
    print("get_create")

    # Use fast cache if it exists
    data = cache.get('standings')
    if not data:
        standings_url = "http://api.sportradar.us/nba-t3/seasontd/2015/PST/standings.json"
        params = {'api_key': 'pa8j2hgacuvgkavsz5zfna7n'}
        try:
            standings_response = requests.get(standings_url, params)
            data = standings_response.json()
            cache.set('standings', data, 120)
            messages.append("Set cache")
        except ValueError as e:
            print(e)
            err.append(e)
            time.sleep(1)
            standings_response = requests.get(standings_url, params)
            data = standings_response.json()
            cache.set('standings', data, 120)
            messages.append("Set cache")
            pass
    else:
        messages.append("Using cached data")

    data = data["conferences"]

    for conf in data:
        div = conf["divisions"]
        for d in div:
            team_data = d["teams"]
            for team in team_data:
                team_name = str(team["market"]) + " " + str(team["name"])
                if search_term in team_name:
                    team_id = team["id"]
                    team_wins = int(team["wins"])
                    team_losses = int(team["losses"])

                    messages.append("Creating new model for " + team_name)

                    newTeam, created = Team.objects.get_or_create(
                        pk=team_id,
                        defaults={
                            'name': team_name,
                            'wins': team_wins,
                            'losses': team_losses,
                        }
                    )
                    if created:
                        messages.append("Created Team " + newTeam.name)
                    else:
                        messages.append("Team already exists")

                    return newTeam, created

    return None, False


def get_daily_sched():
    print("get_daily_sched")
    today = timezone.now()

    data = cache.get('daily_schedule')
    if not data:
        daily_sched_url = "http://api.sportradar.us/nba-t3/games/2016/" + str(today.month) + "/" + str(today.day) + "/schedule.json"
        params = {'api_key': 'pa8j2hgacuvgkavsz5zfna7n'}
        try:
            daily_sched_response = requests.get(daily_sched_url, params)
            data = daily_sched_response.json()
            cache.set('daily_schedule', data)
        except ValueError as e:
            print(e)
            time.sleep(1)
            daily_sched_response = requests.get(daily_sched_url, params)
            data = daily_sched_response.json()
            cache.set('daily_schedule', data)
            pass
    else:
        print("using cached data")

    count = 0

    for g in data["games"]:
        count += 1

        # Check for non US
        if not g["venue"]["country"] == 'USA':
            g["venue"]["zip"] = ''
            g["venue"]["state"] = ''

        # Save Venue first if it does not exist due to Foreign key constraint
        venue, created = Venue.objects.get_or_create(
            pk=g["venue"]["id"],
            defaults={
                'name': g["venue"]["name"],
                'capacity': int(g["venue"]["capacity"]),
                'city': g["venue"]["city"],
                'zip': g["venue"]["zip"],
                'country': g["venue"]["country"],
                'state': g["venue"]["state"],
                'address': g["venue"]["address"],
            }
        )
        # Check away team to see if it is in the DB. If not, create it
        away, new = get_create_team(g["away"]["name"], messages=[], err=[])
        home, new = get_create_team(g["home"]["name"], messages=[], err=[])

        # Create game instance
        game, created = Game.objects.get_or_create(
            pk=g["id"],
            defaults={
                'date': g["scheduled"],
                'status': g["status"],
                'venue': venue,
                'away_team': away,
                'home_team': home,
            }
        )
    return count


def check_game_winner(wagyr, user):
    boxscore_url = "http://api.sportradar.us/nba-t3/games/" + str(wagyr.game_id.event_id) + "/boxscore.json"
    params = {'api_key': 'pa8j2hgacuvgkavsz5zfna7n'}
    try:
        boxscore_response = requests.get(boxscore_url, params)
        data = boxscore_response.json()
    except ValueError as e:
        print(e)
        time.sleep(1)
        boxscore_response = requests.get(boxscore_url, params)
        data = boxscore_response.json()
        pass

    if data['status'] == 'closed':
        print("game over, update the wagyr")
        # determine the winner of the wagyr
        if data['home']['points'] > data['away']['points']:
            winner = data['home']['name']
        else:
            winner = data['away']['name']

        if wagyr.self_id.username == user.username:
            if winner.title() in wagyr.self_team.title():
                wagyr.wagyr_winner = user
                wagyr.status = wagyr.PENDING_OPPONENT
                wagyr.save()
            else:
                wagyr.wagyr_winner = wagyr.opponent_id
                wagyr.status = wagyr.PENDING_SELF
                wagyr.save()
        else:
            if winner.title() in wagyr.self_team.title():
                wagyr.wagyr_winner = wagyr.opponent_id
                wagyr.status = wagyr.PENDING_SELF
                wagyr.save()
            else:
                wagyr.wagyr_winner = user
                wagyr.status = wagyr.PENDING_OPPONENT
                wagyr.save()