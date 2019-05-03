from wtforms import StringField, IntegerField
from wtforms.validators import Email,InputRequired, Length, EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6, 20, message="密码长度6至20位")])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message="旧密码长度6至20位")])
    newpwd = StringField(validators=[Length(6, 20, message="新密码长度6至20位")])
    newpwd2 =  StringField(validators=[EqualTo("newpwd", message="确认密码必须和新密码一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式邮箱!")])
    captcha = StringField(validators=[InputRequired("请输入验证码!")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.strip().lower() != captcha_cache.lower():
            raise ValidationError("验证码错误!")

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("与原邮箱一致!")


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入图片跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入优先级')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID!')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称!')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired('请输入板块ID!')])
