from django.conf.urls import url

from game import views as team_views

urlpatterns = [
    url(r'^teams/(?P<pk>\d+)/$', team_views.view_team, name='view_team'),
    url(r'^teams/$', team_views.TeamListView.as_view(), name='list_teams'),
    url(r'^get_teams', team_views.get_teams, name='get_teams'),
    url(r'^players/$', team_views.PlayerListView.as_view(), name='list_players'),
    url(r'^schedule/$', team_views.schedule, name='schedule'),
    url(r'^schedule/update_schedule/$', team_views.update_schedule, name='update_schedule'),
]
