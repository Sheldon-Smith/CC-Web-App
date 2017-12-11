"""CCSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from stats import views as stats_views

urlpatterns = [
    url(r'^create_game/$', stats_views.create_game_view, name='create_game_view'),
    url(r'^game/$', stats_views.game_view, name='game_view'),
    url(r'^init_game_logic/$', stats_views.init_game_logic, name='init_game_logic'),
    url(r'^shot_logic/$', stats_views.shot_logic, name='shot_logic'),
    url(r'^quit_logic/$', stats_views.quit_game_logic, name='quit_game_logic'),
    url(r'^game_state/$', stats_views.game_state, name='game_state'),
    url(r'^pull_logic/$', stats_views.pull_logic, name='pull_logic'),
    url(r'^undo_logic/$', stats_views.undo_logic, name='undo')
]
