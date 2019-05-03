from flask import (Blueprint, views, render_template,
                   request, session, redirect, url_for, g,
                   jsonify)

from .forms import (LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm,
                    UpdateBannerForm, AddBoardForm, UpdateBoardForm)

from .models import CMSUser, CMSPermission
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, zlcache
import string
import random
from tasks import send_mail



bp = Blueprint("cms", __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    # /email_captcha/?email=xxx@qq.com
    email = request.args.get('email')
    if not email:
        return restful.paramError('请输入邮箱参数')
    # 发邮件
    source = list(string.ascii_letters)
    source.extend(list(map(str, range(0,10))))
    captcha = "".join(random.sample(source, 6))
    # message = Message('BBS邮箱验证码', recipients=[email], body=f"您的验证码是: {captcha}\n【10分钟之内有效】" )
    # try:
    #     mail.send(message)
    # except:
    #     return restful.serverError()

    send_mail.delay('LGF_BBS邮箱验证码',[email], f"您的验证码是: {captcha}\n【10分钟之内有效】" )
    zlcache.set(email,captcha)

    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.poster)
def posts():
    postList = PostModel.query.all()

    return render_template('cms/cms_posts.html', posts=postList)



@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.poster)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.paramError('请输入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramError('该帖子不存在!')
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.poster)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.paramError('请输入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramError('该帖子不存在!')
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.comments)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.boarder)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards':board_models
    }
    return render_template('cms/cms_boards.html', **context)



@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.boarder)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    return restful.paramError(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.boarder)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        return restful.paramError(message='该板块不存在!')

    return restful.paramError(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.boarder)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.paramError('请输入板块ID!')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.paramError(message='该板块不存在!')
    db.session.delete(board)
    db.session.commit()
    return restful.success()



@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.frontUser)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.cmsUser)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/banners/')
@login_required
def banners():
    banner = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banner=banner)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    return restful.paramError(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramError(message='没有该图片!')

    return restful.paramError(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanenr():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.paramError(message='请输入轮播图ID')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.paramError(message='没有该图片!')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()



class LoginView(views.MethodView):
    def get(self, message=None):
         return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True  # Cookie过期时间31天
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')

        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetPassword.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200, "message":""})
                return restful.success()
            else:
                return restful.paramError("旧密码错误")
        else:
            # message = form.get_error()
            # return jsonify({"code":400, "message":message})
            return restful.paramError(form.get_error())


class ResetEmail(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetEmail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramError(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmail.as_view('resetemail'))

