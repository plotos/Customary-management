from werkzeug.security import generate_password_hash, check_password_hash
from demo import db
from flask_login import UserMixin

# 用户信息表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户id
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

# 习惯信息表
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 习惯id
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))  # 习惯属于的用户
    habit_name = db.Column(db.String(20))  # 习惯名称
    records = db.relationship('Record', backref='habit', lazy=True, cascade='all, delete-orphan', passive_deletes = True) # 包含的习惯记录

# 习惯记录表
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录条目id
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))  # 记录属于的用户id
    date = db.Column(db.Date)  # 日期
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id', ondelete = 'CASCADE'))  # 习惯id
    habit_name = db.Column(db.String(20))  # 习惯名称
    remark = db.Column(db.Text)  # 备注 
    is_complete = db.Column(db.String(1))  # 是否完成
