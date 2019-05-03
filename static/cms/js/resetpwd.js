
$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();    // 是为了阻止按钮默认的提交表单的时间
        var oldPwdElement = $("input[name=oldpwd]");
        var newPwdElement = $("input[name=newpwd]");
        var newPwdElement2 = $("input[name=newpwd2]");

        var oldPwd = oldPwdElement.val();
        var newPwd = newPwdElement.val();
        var newPwd2 = newPwdElement2.val();

        // 1.在模板meta标签中渲染一个csrf-token
        // 2.在AJAX请求头部中，设置 X-CSRFtoken

        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldPwd,
                'newpwd': newPwd,
                'newpwd2': newPwd2
            },

            'success': function (data) {
                // code == 200  Success.
                if (data['code'] === 200) {
                    zlalert.alertSuccessToast("密码修改成功!");
                    oldPwdElement.val("");
                    newPwdElement.val("");
                    newPwdElement2.val("");
                } else {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                    oldPwdElement.val("");
                    newPwdElement.val("");
                    newPwdElement2.val("");
                }
            },

            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });

    });

});