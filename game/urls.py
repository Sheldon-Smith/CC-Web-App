from django.conf.urls import url

from game import views as team_views

urlpatterns = [
    url(r'^teams/(?P<name>\s+)/$', team_views.view_team, name='view_team'),
    url(r'^teams/$', team_views.list_teams, name='list_teams'),
    url(r'^get_teams', team_views.get_teams, name='get_teams'),
]
