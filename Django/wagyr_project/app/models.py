from django.db import models

# Create your models here.
class dailySched(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)

    class Meta:
        def __str__(self):  #For Python 2, use __str__ on Python 3
            return self.month


class Venue(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'venue'


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    wins = models.IntegerField()
    losses = models.IntegerField()
    venue = models.OneToOneField(Venue, db_column='venue', related_name='team_venue')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'team'


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    player_id = models.CharField(max_length=255)
    fname= models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    team = models.ForeignKey(Team, db_column='team', related_name='players')

    def __str__(self):
        return self.fname + ' ' + self.lname

    class Meta:
        managed = True
        db_table = 'player'


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.CharField(max_length=255)
    home_team = models.ForeignKey(Team, to_field='team_id', related_name='home_team', default=2)
    away_team = models.ForeignKey(Team, to_field='team_id', related_name='away_team', default=1)

    class Meta:
        managed = True
        db_table = 'game'


class Wagyr(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'wagyr'
