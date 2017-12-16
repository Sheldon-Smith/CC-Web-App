from django.conf.urls import url

from game import views as team_views

urlpatterns = [
    url(r'^teams/(?P<name>[\w.@+-]+)/$', team_views.view_team, name='view_team'),
    url(r'^teams/$', team_views.TeamListView.as_view(), name='list_teams'),
    url(r'^get_teams', team_views.get_teams, name='get_teams'),
    url(r'^players/$', team_views.PlayerListView.as_view(), name='list_players')
]
