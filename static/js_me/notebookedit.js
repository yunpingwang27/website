$(document).ready(function () {
    var token = Cookies.get("token");
    var note_content = null;
    var note_category = null;
    $.ajax({
        type: "POST",
        url: '/user_note',
        data: {
            token: token,
            note_content:note_content,
        },
        success: function (data) {
            if (data['status'] === 'success') {
                //$("#logout").removeClass("hidden")
                //$("#login").addClass("hidden")
                //$("#userName").html(data['data']['username'])
                //$("#sidebar").append(`<li><a class="meun-item" href="#datacenter" aria-controls="datacenter" role="tab" data-toggle="tab"><span>资料查询</span></a></li>`);
                //username = data['data']['username'];
                note_content = data['data']['note_content']
                $("#note-content").html(data['data']['note_content'])
            } else {
            }
        },
    });
    $("#save-info-button").click(function () {
        var note_content = $("#note_content").val();
        $.ajax({
            type: "POST",
            url: "/other_note/add",
            data: {
                note_content:note_content,
            },
            success: function (data) {
                if (data['status'] === 'success') {
                    $("#note-content").html(data['data']['note_content']);
                    note_content = data['data']['note_content']
                    alert("success!");
                } else {
                }
            },
        });
    });
})