from django.contrib import admin
from app.models import Team, Player, Game, Wagyr, Venue

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Wagyr)
admin.site.register(Venue)