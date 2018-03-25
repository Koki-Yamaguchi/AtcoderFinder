$(function() {
    $('input[name="タグ"]').change(function() {
        var tags = [];
        var notAC = false
        var isWA = false
        $('input[name="タグ"]:checked').each(function() {
            if ($(this).val() == 'notAC') {
                notAC = true;
            } else if ($(this).val() == 'isWA') {
                isWA = true;
            } else {
                tags.push($(this).val());
            }
        });
        console.log(notAC);
        $('table').find('> tbody > tr').each(function() {
            if (isWA && $(this).hasClass('WA') == false) {
                $(this).hide();
            } else if (notAC && $(this).hasClass('AC')) {
                $(this).hide();
            } else {
                cell = $($(this).children('td')[2]);
                var all_match = true;
                for (var i = 0; i < tags.length; i ++) {
                    if (cell.text().indexOf(tags[i]) == -1) {
                        all_match = false;
                    }
                }
                if (all_match) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            }
        });
    });
});
