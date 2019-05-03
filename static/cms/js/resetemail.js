
$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if (!email) {
            zlalert.alertInfoToast("请输入邮箱");
            return;
        }

        zlajax.get({
            'url':'/cms/email_captcha/',
            'data': {
                'email':email
            },

            'success': function (data) {
                if (data['code'] === 200) {
                    zlalert.alertSuccessToast('邮箱发送成功,请注意查收')
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },

            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});


$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailElement = $("input[name='email']");
        var captchaElement = $("input[name='captcha']");

        var email = emailElement.val();
        var captcha = captchaElement.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },

            'success': function (data) {
                if (data['code'] === 200) {
                    zlalert.alertSuccessToast("邮箱修改成功!");
                    emailElement.val("");
                    captchaElement.val("");
                } else{
                    zlalert.alertInfo(data['message']);
                }
            },

            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });


    })
});

