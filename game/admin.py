from django.contrib import admin

from .models import Team, Game, Season, Score


class PlayerInline(admin.TabularInline):
    model = Team.players.through


class StatkeeperInline(admin.TabularInline):
    model = Team.statkeepers.through


class ScheduleInline(admin.TabularInline):
    model = Game


class SeasonAdmin(admin.ModelAdmin):
    inlines = [
        ScheduleInline
    ]

    list_display = ['name', 'year']


class TeamAdmin(admin.ModelAdmin):
    inlines = [
        PlayerInline,
        StatkeeperInline,
    ]

    list_display = ['get_name',
                    'wins',
                    'losses',
                    'captain',
                    'keeper']


class ScoreAdmin(admin.ModelAdmin):

    list_display = ['user',
                    'game']

    list_filter = ['user',
                   'game']


admin.site.register(Team, TeamAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Game)
admin.site.register(Score, ScoreAdmin)
