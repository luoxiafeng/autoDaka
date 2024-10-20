from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 数据库连接函数
def get_user(username):
    conn = sqlite3.connect('user_auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# 初始化数据库并创建订单表
def init_db():
    conn = sqlite3.connect('user_auth.db')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')

    # 创建订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            name TEXT,
            profession TEXT,
            address TEXT,
            days TEXT NOT NULL,
            report TEXT NOT NULL,
            time TEXT NOT NULL,
            total_days INTEGER NOT NULL
        )
    ''')

    # 插入管理员账号
    cursor.execute('SELECT * FROM users WHERE username=?', ('admin',))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
                       ('admin', 'admin456@@', '管理员'))

    conn.commit()
    conn.close()

# 保存订单数据到数据库
def save_order(data):
    conn = sqlite3.connect('user_auth.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (account, password, email, name, profession, address, days, report, time, total_days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['account'], data['password'], data.get('email'), data.get('name'), 
          data.get('profession'), data.get('address'), data['days'], data['report'], 
          data['time'], data['total_days']))

    conn.commit()
    conn.close()

# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        
        if user and user[2] == password:  # 密码验证
            session['username'] = username
            session['user_type'] = user[3]
            return redirect(url_for('home'))
        else:
            flash('用户名或密码错误')

    return render_template('login.html')

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', title='首页', username=session['username'])
    return redirect(url_for('login'))

# 退出路由
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# 职校家园表单页面路由
@app.route('/zhixun', methods=['GET', 'POST'])
def zhixun():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        email = request.form.get('email')
        name = request.form.get('name')
        profession = request.form.get('profession')
        address = request.form.get('address')
        days = ','.join(request.form.getlist('days'))
        report = request.form['report']
        time = request.form['time']
        total_days = request.form['total_days']

        # 保存订单信息
        order_data = {
            'account': account,
            'password': password,
            'email': email,
            'name': name,
            'profession': profession,
            'address': address,
            'days': days,
            'report': report,
            'time': time,
            'total_days': total_days
        }

        try:
            save_order(order_data)
            flash('订单创建成功！')
            return redirect(url_for('zhixun'))
        except Exception as e:
            flash('订单创建失败，请重试！')
            print(e)

    return render_template('zhixun.html')

# 学习通表单页面路由
@app.route('/xuexitong', methods=['GET', 'POST'])
def xuexitong():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        email = request.form.get('email')
        name = request.form.get('name')
        profession = request.form.get('profession')
        address = request.form.get('address')
        days = ','.join(request.form.getlist('days'))
        report = request.form['report']
        time = request.form['time']
        total_days = request.form['total_days']

        # 保存订单信息
        order_data = {
            'account': account,
            'password': password,
            'email': email,
            'name': name,
            'profession': profession,
            'address': address,
            'days': days,
            'report': report,
            'time': time,
            'total_days': total_days
        }

        try:
            save_order(order_data)
            flash('学习通订单创建成功！')
            return redirect(url_for('xuexitong'))
        except Exception as e:
            flash('订单创建失败，请重试！')
            print(e)

    return render_template('xuexitong.html')

@app.route('/gongxueyun', methods=['GET', 'POST'])
def gongxueyun():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        email = request.form.get('email')
        name = request.form.get('name')
        profession = request.form.get('profession')
        address = request.form.get('address')
        days = ','.join(request.form.getlist('days'))
        report = request.form['report']
        time = request.form['time']
        total_days = request.form['total_days']

        # 保存订单信息到数据库
        order_data = {
            'account': account,
            'password': password,
            'email': email,
            'name': name,
            'profession': profession,
            'address': address,
            'days': days,
            'report': report,
            'time': time,
            'total_days': total_days
        }

        try:
            save_order(order_data)
            flash('工学云订单创建成功！')
            return redirect(url_for('gongxueyun'))
        except Exception as e:
            flash('订单创建失败，请重试！')
            print(e)

    return render_template('gongxueyun.html')


# 启动应用前初始化数据库
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
