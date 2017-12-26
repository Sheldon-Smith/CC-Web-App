function update_schedule (season, week, schedule) {
   $.ajax({
        url: '/schedule/update_schedule/',
        method: 'GET',
        data: {'season': season, 'week': week.children('.week-page').text()},
        success: function(data) {
            schedule.empty();
            $.each(data['schedule'], function (index, week) {
                home_division = (week.home_team[0].division === 'Blue') ? "Blue" : "Pink";
                away_division = (week.away_team[0].division === 'Blue') ? "Blue" : "Pink";
                schedule.append('<tr><td style="background-color: ' + home_division + ';">' + week.home_team[0].name + '</td>' + '<td style="background-color: ' + away_division + ';">' + week.away_team[0].name + '</td>');
            });
            var week_container = week.parent();
            var id = week.attr('id');
            week_container.empty();
            $.each(data['weeks'], function (index, week) {
                week_container.append('<li class="page-item" id=' + week + '><a href="#" class="page-link week-page">' + week + '</a></li>');
            });
            week = $('#' + id);
            week.attr('class', 'page-item active');
        }
    });
}


$(document).ready(function () {
    var seasons = $('#seasons');
    var schedule = $('#schedule');
    var week = $('.page-item.active');

    update_schedule(seasons.val(), week, schedule);
    seasons.change(function () {
        update_schedule(seasons.val(), week, schedule)
    });

    $('.pagination').on('click', '.page-item', function () {
       week.attr('class', 'page-item');
       week = $(this);
       var id = week.attr('id');
       $("#" + id).attr('class', 'page-item active');
       update_schedule(seasons.val(), week, schedule);
    });
});