
/**
 * statsArray structure first index is team then player then stats i.e. [[team1[player1[top]][team2[player1[top]]]]
 * @param statsArray
 */
function updateStats(statsArray) {
    for (var i = 1; i <= statsArray[0].length; i++) {
        $("#home_player"+i+"_top").text(statsArray[0][i-1][0]);
        $("#home_player"+i+"_topGay").text(statsArray[0][i-1][1]);
        $("#home_player"+i+"_bottom").text(statsArray[0][i-1][2]);
        $("#home_player"+i+"_bottomGay").text(statsArray[0][i-1][3]);
        $("#home_player"+i+"_miss").text(statsArray[0][i-1][4]);
        $("#home_player"+i+"_percent").text(statsArray[0][i-1][5] + "%");

        $("#away_player"+i+"_top").text(statsArray[1][i-1][0]);
        $("#away_player"+i+"_topGay").text(statsArray[1][i-1][1]);
        $("#away_player"+i+"_bottom").text(statsArray[1][i-1][2]);
        $("#away_player"+i+"_bottomGay").text(statsArray[1][i-1][3]);
        $("#away_player"+i+"_miss").text(statsArray[1][i-1][4]);
        $("#away_player"+i+"_percent").text(statsArray[1][i-1][5] + "%");
    }
}

function get_state(data) {
    $("#current_player").text(data['current_player']);
    if (data['home_cups'] > 0) {
        $("#home_progress").text(data['home_cups'])
    } else {
        $("#home_progress").text("")
    }
    if (data['away_cups'] > 0) {
        $("#away_progress").text(data['away_cups'])
    } else {
        $("#away_progress").text("")
    }
    $("#home_progress").css("width", data['home_percent'] + "%").prop("aria-valuenow", data['home_percent']);
    $("#away_progress").css("width", data['away_percent'] + "%").prop("aria-valuenow", data['away_percent']);
    $("#cups_hit").text(data['cups_hit']);
    $("#to_drink").text(data['to_drink']);
    updateStats(data['stats_array']);
}

function next_round() {
    $.ajax({
        type: "GET",
        url: "/stats/game_state/",
        success: function (data) {
            if(data['game_over']) {
                window.location.replace(data.redirect);
                return;
            }
            get_state(data);
        }
    });
}

function shot(shotArray) {
    $.ajax({
        type: "POST",
        url: '/stats/shot_logic/',
        data: JSON.stringify({'shot_data': shotArray}),
        success: next_round
    })
}
$(document).ready(function () {

    next_round();

    $("#pull_home").click(function () {
        $.ajax({
            type: "POST",
            url: '/stats/pull_logic/',
            data:  JSON.stringify({'team': 0}),
            success: next_round
        })
    });

    $("#pull_away").click(function () {
        $.ajax({
            type: "POST",
            url: '/stats/pull_logic/',
            data:  JSON.stringify({'team': 1}),
            success: next_round
        })
    });

    $("#topMake").click(function () {
       var shotArray = [1,0,0,0,0,0];
       shot(shotArray);
    });

    $("#topGay").click(function () {
        var shotArray = [0,1,0,0,0,0];
        shot(shotArray);
    });

     $("#bottomMake").click(function () {
        var shotArray = [0,0,1,0,0,0];
        shot(shotArray);
    });

    $("#bottomGay").click(function () {
        var shotArray = [0,0,0,1,0,0];
        shot(shotArray);
    });

    $("#miss").click(function () {
        var shotArray = [0,0,0,0,1,0];
        shot(shotArray);
    });

    $("#quit_no_save").click(function () {
        $.ajax({
            url: '/stats/quit_logic/',
            method: "POST",
            data: {'save': 0},
            success: function (data) {
                window.location.href = data['redirect'];
            }
        });
    });

    $("#quit_save").click(function () {
        $.ajax({
            url: '/stats/quit_logic/',
            method: "POST",
            data: {'save': 1},
            success: function (data) {
                window.location.href = data['redirect'];
            }
        });
    });

    $("#undo").click(function() {
        $.ajax({
            url: '/stats/undo_logic/',
            method: "POST",
            success: next_round
        });
    });

});