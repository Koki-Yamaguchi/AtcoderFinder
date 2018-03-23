$(function(){
    $('#btn').click(function(){
        var user = $('#userid [name=user]').val();
        if (user == "") {
            return;
        }
        var filename = "./json/users/" + user + ".json";
        $.getJSON(filename, function(data) {
            console.log('IN')
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
});
