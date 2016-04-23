from django.db import models
from django.db.models import Q
from django.utils import timezone

'''
from django.contrib.auth import User
'''


class Wagyr(models.Model):
	wagyr_id=models.CharField(max_length=255, primary_key=True)
	user1_id=models.CharField(max_length=255, null=True)
	user2_id=models.CharField(max_length=255, null=True)
	game_id=models.CharField(max_length=255, null=True)
	
	class Meta:
        	managed = True
        	db_table = 'wagyr'


class Venue(models.Model):
    venue_id = models.CharField(max_length=255, primary_key=True)
    city = models.CharField(max_length=255, null=True)
    capacity = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.country == 'USA':
            return self.name + ' in ' + self.city + ', ' + self.state
        else:
            return self.name + ' in ' + self.city + ', ' + self.country

    class Meta:
        managed = True
        db_table = 'venue'


class Team(models.Model):
    team_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    wins = models.IntegerField(null=True, blank=True)
    losses = models.IntegerField(null=True, blank=True)
    venue = models.OneToOneField(Venue, db_column='venue', related_name='team_venue', null=True, blank=True)

    def is_sched_loaded(self):
        """
        This is a 'cheap' fix to this problem.  Check to see if there are 82-(W+L) games in the DB
        :return: Bool
        """
        games_left = 82 - (self.wins + self.losses)
        games_in_db = Game.objects.filter(Q(home_team__name=self.name) | Q(away_team__name=self.name)).count()

        if games_left > games_in_db:
            fetched = False
        else:
            fetched = True

        return fetched

    def get_record(self):
        self.wins = 40
        self.losses = 30
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'team'


class Player(models.Model):
    player_id = models.CharField(max_length=255, primary_key=True)
    fname= models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    team = models.ForeignKey(Team, db_column='team', related_name='players')

    class Meta:
        managed = True
        db_table = 'player'


class Game(models.Model):
    event_id = models.CharField(primary_key=True, max_length=255)
    home_team = models.ForeignKey(Team, to_field='team_id', related_name='home_team')
    away_team = models.ForeignKey(Team, to_field='team_id', related_name='away_team')
    date = models.DateTimeField(default=timezone.now)
    venue = models.ForeignKey(Venue, to_field='venue_id', related_name='game_venue')
    status = models.CharField(max_length=255, default='scheduled')

    def get_search_team(self, search_term):
        if search_term in self.home_team.name:
            return self.home_team
        if search_term in self.away_team.name:
            return self.away_team

    def __str__(self):
        return str(self.home_team) + ' vs ' + str(self.away_team)

    class Meta:
        managed = True
        db_table = 'game'
        ordering = ['date']

'''
class Wagyr(models.Model):
    id = models.AutoField(primary_key=True)
    #creted = models.Foreign(WgyrUser, to_field='usernme', nme='creter')
    #invited = models.ForeignKey(WgyrUser, to_field='usernme', nme='invited')
    wager = models.IntegerField()
    #completed = models.NullBoolenField()
    winner = models.ForeignKey('self', defult=some_func)

    class Meta:
        managed = True
        db_table = 'wagyr'
	'''
