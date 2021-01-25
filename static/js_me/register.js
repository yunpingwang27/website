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
                username = data['data']['username'];
                type = data['data']['type']
            } else {
            }
        },
    });


    $("#register-button").click(function () {
        var username = $("#username-signup").val();
        var password = $("#password-signup").val();
        var passwordRepeat = $("#password-confirm-signup").val();
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
            success: function (data) {
                if (data['data']==='invalid username'){
                    alert("用户名中不能有空格");
                    return;
                }
                if (data['data']==='duplicated username'){
                    alert("用户名已被占用");
                    return;
                }
                if (data['data']==='password length should be between 8 and 16'){
                    alert("密码长度应当在8到16位之间");
                    return;
                }
                if (data['data']==='Invalid password'){
                    alert("密码中不能有空格");
                    return;
                }
                alert("success!");
                window.location.href = "/login.html";
            },
        });
    });
})
