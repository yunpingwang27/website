$(document).ready(function () {
    var token = Cookies.get("token");
    //var event_time = null;
    var process_name = null;
    var process_brief_intro = null;
    $.ajax({
        type: "POST",
        url: '/user_process',
        data: {
            token: token,
        },

        success: function (data) {
            if (data['status'] === 'success') {
                alert('success');
                // $("#process-name").html(data['data']['process_name']);
                // $("#process-brief-intro").html(data['data']['process_brief_intro'])
                // $('progress-content').insertAfter('progress-content');
                process_name = data['data']['process_name'];
                process_brief_intro = data['data']['process_brief_intro'];
            } else {
                alert(data['data']);
            }
        },
    });

    $("#add-process").click(function () {
        var process_name = $("#new-process-name").val();
        var process_brief_intro = $("#new-process-brief-intro").val();
        token = Cookies.get('token');
        $.ajax({
            type: "POST",
            url: '/process_add',
            data: {
                process_name:process_name,
                process_brief_intro:process_brief_intro,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    // $('.process-sample').append($(this).clone());
                    $('.process-sample').append('<p>学</p>');
                    // $(".word").append($(this).clone()); 
                    alert('success');
                    alert(data);
                    // alert(data);
                    // $("#process-name").html(data['data']['process_name']);
                    // $("#process-brief-intro").html(data['data']['process_brief_intro']);
                    //window.location.href = "/taskboard.html";
                } else {
                    alert(data['data']);
                }
            },
        });
    });
})