from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel, PostModel



CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission
FrontUser = front_models.FrontUser

app = create_app()
manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功!')

@manager.command
def create_role():
    # 1. 访问者, 只能修改自己的个人信息..
    visitor = CMSRole(name="访问者", desc="只能访问数据，不能修改")
    visitor.permissions = CMSPermission.visitor

    # 2. 运营角色， 修改个人信息，管理帖子，管理评论，管理前台用户
    operator = CMSRole(name="运营", desc="管理帖子、评论、前台用户")
    operator.permissions = CMSPermission.visitor|CMSPermission.poster|CMSPermission.cmsUser| \
                           CMSPermission.comments|CMSPermission.frontUser

    # 3. 管理员，  拥有绝大部分权限
    admin = CMSRole(name='管理员', desc="拥有本系统所有权限")
    admin.permissions = CMSPermission.visitor|CMSPermission.poster|CMSPermission.frontUser| \
                        CMSPermission.comments|CMSPermission.cmsUser|CMSPermission.boarder

    # 4. 开发者.
    developer = CMSRole(name='开发者', desc='开发人员专用权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('User was added to Role success!')
        else:
            print(f'没有{role}这个角色')
    else:
        print(f"该邮箱({email})不存在")


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_frontUser(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()




@manager.command
def test_permission():
    user = CMSUser.query.filter_by(username='lgf').first()
    # if user.has_permissions(CMSPermission.visitor):
    if user.is_developer:
        print('The User has DEVELOPER permission!')
    else:
        print('The User has not DEVELOPER permission!')


@manager.command
def create_test_post():
    for i in range(1, 200):
        title = f'标题 {i}'
        content = f"内容 {i}"
        board = BoardModel.query.first()
        author = FrontUser.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('Test Posts added successful!')

if __name__ == "__main__":
    manager.run()

