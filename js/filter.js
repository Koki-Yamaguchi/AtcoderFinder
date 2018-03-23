$(function() {
    $('input[name="タグ"]').change(function() {
        var tags = [];
        $('input[name="タグ"]:checked').each(function() {
            tags.push($(this).val());
        });
        $('table').find('> tbody > tr').each(function() {
            cell = $($(this).children('td')[2]);
            //console.log(cell.text())
            //console.log(tags)
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
        });
    });
});
