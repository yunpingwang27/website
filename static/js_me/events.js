$(document).ready(function () {
    var token = Cookies.get("token");
    //var event_time = null;
    var event_name = null;
    var event_type = null;
    $.ajax({
        type: "POST",
        url: '/user_event',
        data: {
            token: token,
            event_name:event_name,
            event_type:event_type,
        },

        success: function (data) {
            if (data['status'] === 'success') {
                event_name = data['data']['event_name'];
                event_type = data['data']['event_type'];
            } else {
            }
        },
    });


    $("#save-events").click(function () {
        var event_name = $("#username-signin").val();
        var event_type = $("select[name=event-bg]:checked").val();
        var token = Cookies.get('token');
        //var event_time = 
        $.ajax({
            type: "POST",
            url: '/event_add',
            data: {
                token:token,
                event_name:event_name,
                event_type:event_type,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    alert('success');
                    Cookies.set('token', data['data']['token']);
                    window.location.href = "/university/events.html";
                } else {
                    alert(data['data']);
                }
            },
        });
    });
})