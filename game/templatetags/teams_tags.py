from django import template

register = template.Library()


@register.simple_tag
def get_team_shot_percentage_for_season(team, season):
    return team.get_shot_percentage(season)
