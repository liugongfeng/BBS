# encoding: utf-8

from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        print("/apps/form.py/ -> self.errors: ", self.errors)
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()