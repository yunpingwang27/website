$(document).ready(function () {
    var token = Cookies.get("token");
    var username = null;
    var type = null;
    var email_address = null;
    var phone_number = null;
    $.ajax({
        type: "POST",
        url: '/user_info',
        data: {
            token: token,
        },

        success: function (data) {
            if (data['status'] === 'success') {
                username = data['data']['username'];
                type = data['data']['type'];
                email_address = ['data']['email_address']
                phone_number =['data']['phone_number']
            } else {
            }
        },
    });


    $("#send-password").click(function () {
        var email_address = $("#exampleInputEmail1").val();
        var phone_number = $("#exampleInputPhone").val();
        $.ajax({
            type: "POST",
            url: '/forgot_password',
            data: {
                email_address: email_address,
                phone_number: phone_number,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    Cookies.set('token', data['data']['token']);
                    window.location.href = "/login.html";
                } else {
                    alert(data['data']);
                }
            },
        });
    });
})