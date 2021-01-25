
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
                $("#logout").removeClass("hidden")
                $("#login").addClass("hidden")
                $("#userName").html(data['data']['username'])
                $("#sidebar").append(`<li><a class="meun-item" href="#datacenter" aria-controls="datacenter" role="tab" data-toggle="tab"><span>资料查询</span></a></li>`);
                username = data['data']['username'];
                type = data['data']['type'];
            } else {
            }
        },
    });

    $("#logout-button").click(function () {
        $.ajax({
            type: "POST",
            url: '/logout',
            data: {
                token: token,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    Cookies.remove('token')
                    window.location.href = "/index.html";
                } else {
                    alert(data['data']);
                }
            },
        });
    });
    $("#register-button").click(function () {
        var username = $("#usename-signup").val();
        var password = $("#password-signup").val();
        var passwordRepeat = $("#password-repeat-signup").val();
        var type = $("input[name=user-type-radio]:checked").val();
        if (type !== "teacher" && type !== "student") {
            alert("请选择用户类型");
            return;
        }
        if (password !== passwordRepeat) {
            alert("两次密码不一致");
            return;
        }
        $.ajax({
            type: "POST",
            url: "/user_register",
            data: {
                username: username,
                password: password,
                type: type
            },
            success: function () {
                window.location.href = "/index.html";
            },
        });
    });
    $("#login-button").click(function () {
        var username = $("#username-signin").val();
        var password = $("#password-signin").val();
        $.ajax({
            type: "POST",
            url: '/user_login',
            data: {
                username: username,
                password: password,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    Cookies.set('token', data['data']['token']);
                    window.location.href = "/studentcenter.html";
                } else {
                    alert(data['data']);
                }
            },
        });
    });
    $("#to-center").click(function () {
        if (type === "student") {
            window.location.href = "/studentcenter.html";
        } else if (type == "teacher") {
            window.location.href = "/teachercenter.html";
        }
    })
})