from flask import Blueprint, request, make_response, jsonify
from utils import restful, zlcache, juheshuju
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO
import qiniu, os
from tasks import send_sms_captcha

bp = Blueprint("common", __name__, url_prefix='/c')

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # /c/sms_captcha/xxx
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.paramError('请输入手机号码')
#
#     captcha = Captcha.gene_text(number=4)
#
#     # 验证码发送成功
#     if alidayu.send_sms(telephone, code=captcha):
#         return restful.success()
#     else:
#         # return restful.paramError(message='验证码发送失败!')
#         return restful.success()


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # telephone , timeStamp
    # md5(timeStamp + telephone + salt)
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        zlcache.set(telephone, captcha.lower())
        send_sms_captcha(telephone, captcha)
        return restful.success()
        # print(f"短信验证码: {captcha}", type(captcha))
        # if juheshuju.send(telephone, captcha=captcha):
        #     zlcache.set(telephone, captcha.lower())
        #     print(f"发送成功, 短信验证码: {captcha}", type(captcha))
        #     return restful.success()
        # else:
        #     # print(f"发送失败, 短信验证码: {captcha}", type(captcha))
        #     return restful.paramError('发送失败,请稍后再试!')
    return restful.paramError(message='参数错误!')


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    print(text, image)
    zlcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    q = qiniu.Auth(os.environ.get('QN_KEY'), os.environ.get('QN_SECRET'))
    bucket = 'bbs'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})


