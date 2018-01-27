$(document).ready(function () {
   $.ajax({
       type: "GET",
       url: 'team_schedule',
       success: function (data) {
          var schedule = $('#schedule_body');
          schedule.empty();
          $.each(data['schedule'], function (index, week) {
                home_division = (week.home_team[0].division === 'Blue') ? "Blue" : "Pink";
                away_division = (week.away_team[0].division === 'Blue') ? "Blue" : "Pink";
                schedule.append('<tr class="game" data-href="/stats/create_game?game=' + week.game_id + '"><td style="background-color: ' + home_division + ';">' + week.home_team[0].name + ' \
                    </td>' + '<td style="background-color: ' + away_division + ';">' + week.away_team[0].name + '</td></a></tr>');
            });
          console.log(data);

        }
      })
   });