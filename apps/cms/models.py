from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPermission:
    # 255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b_1111_1111
    # 1. 访问者权限
    visitor = 0b_0000_0001

    # 2. 管理帖子
    poster = 0b_0000_0010

    # 3. 管理评论的权限
    comments = 0b_0000_0100

    # 4. 管理板块的权限
    boarder = 0b_0000_1000

    # 5. 管理前台用户的权限
    frontUser = 0b_0001_0000

    # 6. 管理后台用户的权限
    cmsUser = 0b_0010_0000

    # 7. 后台管理权限
    admin = 0b_0100_0000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.visitor)
    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0

        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def has_permissions(self, permission) -> bool:
        # all_permissions = self.permissions
        # result = all_permissions & permission == permission
        # return result
        return self.permissions&permission == permission

    @property
    def is_developer(self):
        return self.has_permissions(CMSPermission.ALL_PERMISSION)

    # 密码：对外是password， 对内是 _password
