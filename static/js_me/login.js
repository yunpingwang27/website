$(document).ready(function () {
    var token = Cookies.get("token");
    var username = null;
    var type = null;
    $.ajax({
        type: "POST",
        url: '/user_info',
        data: {
            token: token,
        },

        success: function (data) {
            if (data['status'] === 'success') {
                //$("#userName").html(data['data']['username'])
                username = data['data']['username'];
                type = data['data']['type'];
            }
             else {
            }
        },
    });


    $("#login-button").click(function () {
        var username = $("#username-signin").val();
        var password = $("#password-signin").val();
        $.ajax({
            type: "POST",
            url: '/user_login',
            data: {
                username: username,
                password:password,
            },

            success: function (data) {
                if (data['data']==='invalid username or password'){
                    alert("用户名或密码错误");
                    return;
                }
                if (data['status'] === 'success') {
                    Cookies.set('token', data['data']['token']);
                    if (data['data']['type'] === 'teacher'){
                    window.location.href = "/teacher/index.html";
                    }
                    if (data['data']['type'] ==='student'){
                        window.location.href = "/student/index.html";
                    }
                }
                else {
                    alert(data['data']);
                }
            },
        });
    });
})