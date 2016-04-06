import requests
from app.models import Game, Venue, Team


def query_api_sched(search_term, messages):
    url = "http://api.sportradar.us/nba-t3/games/2015/REG/schedule.json"
    params = {'api_key': 'wfejyy6af8z84n9u8rdhrcgj'}
    api_response = requests.get(url, params)
    data = api_response.json()
    count = 0

    if search_term != None:
        for g in data["games"]:
            if g["away"]["name"] == search_term or g["home"]["name"] == search_term:
                if g["status"] == "scheduled":
                    # Save Venue first if it does not exist due to Foreign key constraint
                    venue = Venue.objects.filter(venue_id=g["venue"]["id"])
                    if not venue:
                        new_venue = Venue()
                        new_venue.name = g["venue"]["name"]
                        new_venue.capacity = int(g["venue"]["capacity"])
                        new_venue.city = g["venue"]["city"]
                        new_venue.zip = g["venue"]["zip"]
                        new_venue.country = g["venue"]["country"]
                        new_venue.state = g["venue"]["state"]
                        new_venue.address = g["venue"]["address"]
                        new_venue.venue_id = g["venue"]["id"]
                        new_venue.save()

                    # Save Teams first if they do not exist due to Foreign key constraint
                    # TODO (Ryan) make a function to populate the team object with separate API call

                    if search_term == g["home"]["name"]:
                        search_away_team = Team.objects.filter(team_id=g["away"]["id"])
                        if not search_away_team:
                            away_team = Team()
                            away_team.team_id = g["away"]["id"]
                            away_team.name = g["away"]["name"]
                            away_team.venue = Venue.objects.create(city="testing", state="great", venue_id="hjeenl")
                            away_team.wins = 10
                            away_team.losses = 20
                            away_team.save()
                        home_team = Team()
                        home_team.team_id = g["home"]["id"]
                        home_team.name = g["home"]["name"]
                        home_team.venue = Venue.objects.get(venue_id=g["venue"]["id"])
                        home_team.wins = 20
                        home_team.losses = 10
                        home_team.save()
                    else:
                        search_away_team = Team.objects.filter(team_id=g["home"]["id"])
                        if not search_away_team:
                            away_team = Team()
                            away_team.team_id = g["home"]["id"]
                            away_team.name = g["home"]["name"]
                            away_team.venue = Venue.objects.get(venue_id=g["venue"]["id"])
                            away_team.wins = 10
                            away_team.losses = 20
                            away_team.save()
                        home_team = Team()
                        home_team.team_id = g["away"]["id"]
                        home_team.name = g["away"]["name"]
                        home_team.venue = Venue.objects.create(city="Test", state="help", venue_id="343432")
                        home_team.wins = 20
                        home_team.losses = 10
                        home_team.save()

                    # Create a new Game instance

                    game = Game()
                    game.event_id = g["id"]
                    game.date = g["scheduled"]
                    game.status = g["status"]
                    game.venue = Venue.objects.get(venue_id=g["venue"]["id"])
                    game.away_team = Team.objects.get(team_id=g["away"]["id"])
                    game.home_team = Team.objects.get(team_id=g["home"]["id"])
                    count += 1
                    if search_term == g["home"]["name"]:
                        messages.append("Adding new game to the database... " + g["home"]["name"] +  " vs " + g["away"]["name"])
                    else:
                        messages.append("Adding new game to the database... " + g["home"]["name"] + " @ " + g["away"]["name"])
                    game.save()
                    break

        return count
    else:
        return "No search term provided"


