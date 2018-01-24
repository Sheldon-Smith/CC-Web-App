var home_players;
var away_players;
var numPlayers;

function addPlayer() {
    numPlayers++;
    $("#home_team_col").append(
        '<div class="row form-group" id="home_player' + numPlayers + '_row"> \
            <div class="col-md-12"> \
                <label>Player ' + (numPlayers) + ': <select id="home_player'+ (numPlayers) + '" class=\"form-control players\"></label> \
            </div> \
        </div>'
    );
    $("#away_team_col").append(
        '<div class="row form-group" id="away_player' + numPlayers + '_row"> \
            <div class="col-md-12"> \
                <label>Player ' + (numPlayers) + ': <select id="away_player'+ (numPlayers) + '" class=\"form-control players\"></label> \
            </div> \
        </div>'
    );
    $.each(home_players, function (index, player) {
        var home_player = "home_player" + numPlayers;
       $("#"+home_player).append(
           $("<option></option>").text(player[0] + ' ' + player[1]).val(player[2])
       );
    });
    $.each(away_players, function (index, player) {
        var away_player = "away_player" + numPlayers;
       $("#"+away_player).append(
           $("<option></option>").text(player[0] + ' ' + player[1]).val(player[2])
       );
    });
    $("#addPlayerButton").val(numPlayers);
}




$(document).ready(function () {
    var addPlayerButton = $("#addPlayerButton");
    numPlayers = parseInt(addPlayerButton.val());
   $.ajax({
       type: "GET",
       url: '/get_players',
       data: {'home_team_name': $('#home_team_name').text(),
              'away_team_name': $('#away_team_name').text()},
       success: function (data) {
           home_players = data['home_players'];
           away_players = data['away_players'];
           $.each($(".home_players"), function (index, dropdown) {
               dropdown = $(this);
                $.each(home_players, function (index, player) {
                   dropdown.append(
                       $("<option></option>").text(player[0] + ' ' + player[1]).val(player[2])
                   );
               });
           });
           $.each($(".away_players"), function (index, dropdown) {
               dropdown = $(this);
                $.each(away_players, function (index, player) {
                   dropdown.append(
                       $("<option></option>").text(player[0] + ' ' + player[1]).val(player[2])
                   );
               });
           });
       }
   });

   addPlayerButton.click(addPlayer);
   $("#removePlayerButton").click(function () {
       $("#home_player" + numPlayers.toString() + "_row").remove();
       $("#away_player" + numPlayers.toString() + "_row").remove();
       numPlayers--;
       addPlayerButton.val(numPlayers);
   });

   $("#startGame").click(function () {
        var homePlayers = [];
        var awayPlayers = [];
        for(var i = 1; i <= numPlayers; i++) {
          var homePlayer = $("#home_player" + i + ' option:selected');
          var awayPlayer = $("#away_player" + i + ' option:selected');
          homePlayers.push([homePlayer.text(), homePlayer.val()]);
          awayPlayers.push([awayPlayer.text(), awayPlayer.val()]);
        }
        $.ajax({
            type: "POST",
            url: '/stats/init_game_logic/',
            data: JSON.stringify({'home_team_players': homePlayers,
                   'away_team_players': awayPlayers,
                   'home_team_name': $("#home_team_name").text(),
                   'away_team_name': $("#away_team_name").text(),
                   'game_id': $("#game_id").val()
                }),
            success: function (data) {
                window.location.href = data.redirect;
            }

        });
   });

});