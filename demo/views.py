from demo import app, db
from demo.models import User, Record, Habit
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from datetime import date, datetime

# 注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 表单处理
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        check_password = request.form['check_password']

        if(password != check_password):
            flash("两次密码输入不同")
            redirect(url_for('register'))
        
        user_num = User.query.filter_by(username=username).count()
        if user_num == 0:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            redirect(url_for('login'))
        else:
            flash("用户已存在")
            redirect(url_for('register'))

    return render_template('register.html')

# 登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 表单处理
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        try:
            if user.validate_password(password):
                login_user(user)
                return redirect(url_for('today'))
            else:
                flash("密码错误")
                return redirect(url_for('login'))
        except AttributeError:
            flash("用户名不存在")
            redirect(url_for('login'))
            
    return render_template('login.html')

# 登出视图
@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    return redirect(url_for('login'))  # 重定向回首页

# 首页视图，今日视图
@app.route('/')
@app.route('/today')
@login_required
def today():
    now = date.today()

    # 获取填充列表项
    records = []
    new_id = 0
    habits = Habit.query.filter_by(uid=current_user.id)
    for habit in habits:
        if Record.query.filter_by(habit_id=habit.id, date=now).first() == None:
            record = Record(id=new_id, habit_id=habit.id, habit_name=habit.habit_name, remark="无", is_complete="否")
            new_id = new_id - 1
        else:
            record = Record.query.filter_by(habit_id=habit.id, date=now).first()
        records.append(record)

    return render_template('today.html', records=records)

# 今日视图修改表格项
@app.route('/today/<id>/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def today_modify(id, habit_id):
    now = date.today()
    id = int(id)

    # 获取填充列表项
    records = []
    new_id = 0
    habits = Habit.query.filter_by(uid=current_user.id)
    for habit in habits:
        if Record.query.filter_by(habit_id=habit.id, date=now).first() == None:
            record = Record(id=new_id, habit_id=habit.id, habit_name=habit.habit_name, remark="无", is_complete="否")
            new_id = new_id - 1
        else:
            record = Record.query.filter_by(habit_id=habit.id, date=now).first()
        records.append(record)

    #表单处理
    if request.method == "POST":
        habit_name = request.form['habit_name']
        is_complete = request.form['is_complete']
        remark = request.form['remark']
        if id <= 0:
            new_record = Record(uid=current_user.id, date=now, habit_id=habit_id, habit_name=habit_name, remark=remark, is_complete=is_complete)
            db.session.add(new_record)
            db.session.commit()
        else:
            new_record = Record.query.get(id)
            new_record.is_complete = is_complete
            new_record.remark = remark
            db.session.commit()
        return redirect(url_for('today'))

    return render_template('today.html', records=records, id=id)

# 习惯列表视图
@app.route('/habit_list')
@login_required
def habit_list():
    habits = Habit.query.filter_by(uid=current_user.id)
    return render_template('habit_list.html', habits=habits)

# 习惯列表修改视图
@app.route('/habit_list/<int:id>', methods=['GET', 'POST'])
@login_required
def habit_list_modify(id):
    habits = Habit.query.filter_by(uid=current_user.id)

    if request.method == "POST":
        habit_name = request.form['habit_name']
        habit = Habit.query.get(id)
        habit.habit_name = habit_name
        db.session.commit()
        return redirect(url_for('habit_list'))

    return render_template('habit_list.html', habits=habits, id=id)

# 习惯添加视图
@app.route('/habit_list_add')
@login_required
def habit_list_add():
    habit = Habit(uid=current_user.id, habit_name="")
    db.session.add(habit)
    db.session.commit()
    return redirect(url_for('habit_list_modify', id=habit.id))

# 习惯删除视图
@app.route('/habit_list_del/<int:id>')
@login_required
def habit_list_del(id):
    habit = Habit.query.get(id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('habit_list'))

# 历史视图
@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    now = date.today()

    if request.method == "POST":
        now = request.form['now']

    # 获取填充列表项
    records = []
    new_id = 0
    habits = Habit.query.filter_by(uid=current_user.id)
    for habit in habits:
        if Record.query.filter_by(habit_id=habit.id, date=now).first() == None:
            record = Record(id=new_id, habit_id=habit.id, habit_name=habit.habit_name, remark="无", is_complete="否")
            new_id = new_id - 1
        else:
            record = Record.query.filter_by(habit_id=habit.id, date=now).first()
        records.append(record)

    return render_template('history.html', records=records, now=now)

# 历史视图修改表单项
@app.route('/history_modify/<id>/<int:habit_id>/<now_date>', methods=['GET', 'POST'])
@login_required
def history_modify(id, habit_id, now_date):
    id = int(id)
    now = datetime.strptime(now_date, '%Y-%m-%d').date()

    # 获取填充列表项
    records = []
    new_id = 0
    habits = Habit.query.filter_by(uid=current_user.id)
    for habit in habits:
        if Record.query.filter_by(habit_id=habit.id, date=now).first() == None:
            record = Record(id=new_id, habit_id=habit.id, habit_name=habit.habit_name, remark="无", is_complete="否")
            new_id = new_id - 1
        else:
            record = Record.query.filter_by(habit_id=habit.id, date=now).first()
        records.append(record)

    #表单处理
    if request.method == "POST":
        habit_name = request.form['habit_name']
        is_complete = request.form['is_complete']
        remark = request.form['remark']
        if id <= 0:
            new_record = Record(uid=current_user.id, date=now, habit_id=habit_id, habit_name=habit_name, remark=remark, is_complete=is_complete)
            db.session.add(new_record)
            db.session.commit()
        else:
            new_record = Record.query.get(id)
            new_record.is_complete = is_complete
            new_record.remark = remark
            db.session.commit()
        return redirect(url_for('history'))

    return render_template('history.html', id=id, records=records, now=now)
