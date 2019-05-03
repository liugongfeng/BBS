from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Regexp, EqualTo, ValidationError, InputRequired
from utils import zlcache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="手机号码格式有误!")])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}", message='短信验证码错误!')])
    username = StringField(validators=[Regexp(r".{4,20}", message='用户名长度4-20个字符!')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='密码长度6-20位!')])
    password2 = StringField(validators=[EqualTo("password", message='确认密码不一致!')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='图形验证码错误!(Re)')])


    def validate_sms_captcha(self, field):
        # print("类变量: ", self.sms_captcha)
        sms_captcha = field.data
        print("前端传过来的验证码", sms_captcha)
        telephone = self.telephone.data
        sms_captcha_memcached = zlcache.get(telephone)
        print("memcached的验证码", sms_captcha_memcached)
        if not sms_captcha_memcached or sms_captcha_memcached.lower() != sms_captcha.lower():
            raise ValidationError(message='手机验证码错误!(/front/forms/ -> Validate)')


    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_memcached = zlcache.get(graph_captcha.lower())
        if not graph_captcha_memcached:
            raise ValidationError(message='图形验证码错误!(/front/forms/ -> Validate)')


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="手机号码格式有误!")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='密码长度6-20位!')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired('请输入标题!')])
    content = StringField(validators=[InputRequired("请输入内容!")])
    board_id = IntegerField(validators=[InputRequired("请输入板块ID!")])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired("内容不能为空!")])
    post_id = IntegerField(validators=[InputRequired(message="请输入帖子ID")])

