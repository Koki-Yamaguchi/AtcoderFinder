$(function(){
    var get_info = document.location.search;
    var user = get_info.substr(6);
    console.log(user);
    if (user == "") {
        return;
    }
    var url = 'http://kenkoooo.com/atcoder/atcoder-api/results?user=' + user
    $.getJSON(url, function(data) {
        //initialize
        var ac = document.getElementsByClassName('AC');
        var wa = document.getElementsByClassName('WA');
        var no = document.getElementsByClassName('NO');
        for (var i = 0; i < ac.length; i ++) {
            ac[i].classList.remove('AC');
        }
        for (var i = 0; i < wa.length; i ++) {
            wa[i].classList.remove('WA');
        }
        for (var i = 0; i < no.length; i ++) {
            no[i].classList.remove('NO');
        }
        //
        var len = data.length;
        $('table').find('> tbody > tr').each(function() {
            cell = $($(this).children('td')[1]);
            var problem_id = cell.attr("id");
            console.log(problem_id);
            var ac = false;
            var wa = false;
            for (var i = 0; i < len; i++) {
                if (data[i].problem_id == problem_id) {
                    if (data[i].result == "AC") {
                        ac = true;
                        break;
                    } else {
                        wa = true;
                    }
                }
            }
            if (ac) {
                console.log("AC");
                $(this).attr('class', 'AC');
            } else if (wa) {
                console.log("WA");
                $(this).attr('class', 'WA');
            } else {
                console.log("NO");
                $(this).attr('class', 'NO');
            }
        });
        var ac = document.getElementsByClassName('AC');
        var wa = document.getElementsByClassName('WA');
        var no = document.getElementsByClassName('NO');
        for (var i = 0; i < ac.length; i ++) {
            ac[i].style.backgroundColor = "#dff0d8";
        }
        for (var i = 0; i < wa.length; i ++) {
            wa[i].style.backgroundColor = "#fcf8e3";
        }
        for (var i = 0; i < no.length; i ++) {
            no[i].style.backgroundColor = "#FFFFFF";
        }
    });
});
