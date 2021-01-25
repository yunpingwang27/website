$(document).ready(function () {
    // alert("success!");
    var token = Cookies.get("token");
    // var real_name = null;
    // var student_id = null;
    // var phone_number = null;
    // var email_address = null;
    // var qq_number = null;
    // var school_name = null;
    // var grade_name = null;
    // var class_name = null;
    $.ajax({
        type: "POST",
        url: '/user_full_info',
        data: {
            token: token,
        },

        success: function (data) {
            if (data['status'] === 'success') {
                //$("#logout").removeClass("hidden")
                //$("#login").addClass("hidden")
                //$("#userName").html(data['data']['username'])
                // $("#Real-name").html(data['data']['real_name'])
                // $("#Student-id").html(data['data']['student_id'])
                // $("#Phone-number").html(data['data']['phone_number'])
                // $("#Email-address").html(data['data']['email_address'])
                // $("#QQ-number").html(data['data']['qq_number'])
                //$("Real-name").val(data['data']['real_name']);
                // console.log('hello!');
                // alert(data['data']['student_id']);
                $('#Real-name').val("朱均怡");
                $("#Student_id").val(data['data']['student_id']);
                $("#Phone-number").val(data['data']['phone_number']);
                $("#Email-address").val(data['data']['email_address']);
                $('#QQ-number').val(data['data']['qq_number']);

                $("select[name=select-school]:checked").val(data['data']['school_name']);
                $("select[name=select-grade]:checked").val(data['data']['grade_name']);
                $("select[name=select-class]:checked").val(data['data']['class_name']);
                // $("select[name=select-school]:checked").html(data['data']['school_name'])
                // $("select[name=select-grade]:checked").html(data['data']['grade_name'])
                // $("select[name=select-class]:checked").html(data['data']['class_name'])

                //$("#sidebar").append(`<li><a class="meun-item" href="#datacenter" aria-controls="datacenter" role="tab" data-toggle="tab"><span>资料查询</span></a></li>`);
                real_name = data['data']['real_name'];
                student_id = data['data']['student_id'];
                phone_number = data['data']['phone_number'];
                email_address = data['data']['email_address'];
                qq_number = data['data']['qq_number'];
                school_name = data['data']['school_name'];
                grade_name = data['data']['grade_name'];
                class_name = data['data']['class_name'];
            } else {
                alert(data['data']);
            }
        },
    });
    $("#save-info-button").click(function () {
        var token = Cookies.get('token');
        var real_name = $("#Real-name").val();
        var student_id = $("#Student-id").val();
        var phone_number = $("#Phone-number").val();
        var email_address = $("#Email-address").val();
        var qq_number = $("#QQ-number").val();
        //var school_name = document.getElementsById("select-school");
        //var grade_name = $("select[name=select-grade]:checked").val();
        var school_name = $("#School-name").val(); 
        //var school_name = $("#School-name option:selected").val();
        var grade_name = $("#Grade-name").val(); 
        //var grade_name = $('#Grade-name option:selected').val();
        var class_name = $('#Class-name').val();
        alert(email_address);
        //var class_name = $('#Class-name option selected').val();
        //var grade_name = document.getElementById('Grade-name')
        //var class_name = document.getElementsById("select-class");
        if (school_name === "") {
            alert("请选择学校");
            return;
        }
        if (grade_name === "") {
            alert("请选择年级");
            return;
        }
        if (class_name === "") {
            alert("请选择班级");
            return;
        }
        $.ajax({
            type: "POST",
            url: "/user_fill_info",
            data: {
                token:token,
                real_name:real_name,
                student_id:student_id,
                phone_number:phone_number,
                email_address:email_address,
                qq_number:qq_number,
                school_name:school_name,
                grade_name:grade_name,
                class_name:class_name,
            },
            success: function (data) {
                // if (data['data']==='invalid phone number'){
                //     alert("手机号无效");
                //     return;
                // }
                // if (data['data']==='invalid email address'){
                //     alert("邮箱无效");
                //     return;
                // }
                // if (data['data']==='password length should be between 8 and 16'){
                //     alert("密码长度应当在8到16位之间");
                //     return;
                // }
                // if (data['data']==='invalid qq number'){
                //     alert("QQ号无效");
                //     return;
                // }
                if(data['status']==='success'){
                    alert("success!");
                }
                else{
                    alert(data['data']);
                }
            },
        });
    });
    $("#reset-button").click(function(){
        var username = $("#reset-username").val();
        var email_address = $("#reset-email-address").val();
        var phone_number = $("#reset-phone-number").val();
        var old_password = $("#reset-old-password").val();
        var new_password = $("#reset-new-password").val();
        var confirm_password = $('#reset-confirm-password').val()
        if (new_password !== confirm_password) {
            alert("两次密码不一致");
            return;
        }
        $.ajax({
            type: "POST",
            url: "/reset_password",
            data: {
                token:token,
                new_password:new_password,
                old_password:old_password,
                email_address:email_address,
                username:username,
                phone_number:phone_number,
            },
            success: function (data) {
                if (data['data']==='email address is wrong'){
                    alert("邮箱号不正确");
                    return;
                }
                if (data['data']==='phone number is wrong'){
                    alert("手机号不正确");
                    return;
                }
                if (data['data']==='the new password is the same as the old'){
                    alert("新旧密码一致");
                    return;
                }
                if (data['data']==='the length of password should be between 8 and 16'){
                    alert("密码长度应在8到16位之间");
                    return;
                }
                if (data['data']==='illegal character in password'){
                    alert("密码中不能有空格");
                    return;
                }
                if (data['data']==='invalid password'){
                    alert("原密码错误");
                    return;
                }
                if(data['status']==='success'){
                    alert('success');
                    window.location.href='/student/setting.html';
                }else{
                    alert(data['data']);
                }
                // alert("success!");
                // window.location.href = "/student/setting.html";
            },
        });
    });
    })
    