from django.db import models
from django.utils import timezone


class Venue(models.Model):
    venue_id = models.CharField(max_length=255, primary_key=True)
    city = models.CharField(max_length=255, null=True)
    capacity = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.city + ', ' + self.state

    class Meta:
        managed = True
        db_table = 'venue'


class Team(models.Model):
    team_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    wins = models.IntegerField(null=True, blank=True)
    losses = models.IntegerField(null=True, blank=True)
    venue = models.OneToOneField(Venue, db_column='venue', related_name='team_venue')

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

    def __str__(self):
        return self.fname + ' ' + self.lname

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

    def __str__(self):
        return str(self.away_team) + ' @ ' + str(self.home_team)

    class Meta:
        managed = True
        db_table = 'game'


class Wagyr(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'wagyr'
