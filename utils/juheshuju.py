#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

def send(telephone, captcha):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": telephone,  # 接受短信的用户手机号码
        "tpl_id": "155104",  # 您申请的短信模板ID，根据实际情况修改
        "tpl_value": "#code#="+captcha,  # 您设置的模板变量，根据实际情况修改
        "key": "15376982813606a82a071d80998285d3",  # 应用APPKEY(应用详细页查询)
    }
    response = requests.get(url, params=params)
    result = response.json()
    if result['error_code'] == 0:
        return True
    return False



