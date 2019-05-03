from flask import jsonify


class HttpCode:
    ok = 200
    authError = 401
    paramError = 400
    serverError = 500


def restfulResult(code, message, data):
    return jsonify({ "code":code, "message":message, "data":data or {} })

def success(message="", data=None):
    return restfulResult(code=HttpCode.ok, message=message, data=data)

def authError(message=""):
    return restfulResult(code=HttpCode.authError, message=message, data=None)

def paramError(message=""):
    return restfulResult(code=HttpCode.paramError, message=message, data=None)

def serverError(message=""):
    return restfulResult(code=HttpCode.serverError, message=message or "服务器错误", data=None)

