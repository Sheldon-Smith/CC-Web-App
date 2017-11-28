from django.conf.urls import url

from teams import views as team_views

urlpatterns = [
    url(r'^teams/(?P<name>\s+)/$', team_views.view_team, name='view_team'),
    url(r'^teams/$', team_views.list_teams, name='list_teams'),
]
