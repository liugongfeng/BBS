from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired
import hashlib


class SMSCaptchaForm(BaseForm):
    salt = "abcd1234"
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}")])
    timeStamp = StringField(validators=[regexp(r"\d{13}")])
    # sign = md5(telephone + timeStamp + salt)
    sign = StringField(validators=[InputRequired(message="请输入!")])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timeStamp = self.timeStamp.data
        sign = self.sign.data
        # md5(timeStamp + telephone + salt) ;     md5函数必须要传入Byte类型字符串
        sign2 = hashlib.md5((timeStamp + telephone + self.salt).encode('utf-8')).hexdigest()
        return sign == sign2