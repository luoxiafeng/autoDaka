from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('user_auth.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库并创建代理表
def init_db():
    conn = get_db_connection()
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

    # 创建代理表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            account TEXT NOT NULL,
            password TEXT NOT NULL,
            level INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (account, password, email, name, profession, address, days, report, time, total_days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['account'], data['password'], data.get('email'), data.get('name'), 
          data.get('profession'), data.get('address'), data['days'], data['report'], 
          data['time'], data['total_days']))

    conn.commit()
    conn.close()

# 下级代理页面路由
@app.route('/agents')
def agents():
    conn = get_db_connection()
    agents = conn.execute('SELECT * FROM agents').fetchall()
    conn.close()
    return render_template('agents.html', agents=agents)

# 添加代理路由
@app.route('/add_agent', methods=['POST'])
def add_agent():
    nickname = request.form['nickname']
    account = request.form['account']
    password = request.form['password']
    level = request.form['level']

    conn = get_db_connection()
    conn.execute('INSERT INTO agents (nickname, account, password, level) VALUES (?, ?, ?, ?)',
                 (nickname, account, password, level))
    conn.commit()
    conn.close()

    flash('代理添加成功！')
    return redirect(url_for('agents'))

# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        conn.close()
        
        if user and user['password'] == password:  # 密码验证
            session['username'] = username
            session['user_type'] = user['user_type']
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

# 订单页面路由
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

@app.route('/xixunyun')
def xinxiang():
    return render_template('xixunyun.html')

@app.route('/xiaoyoubang')
def xiaoyoubang():
    return render_template('xiaoyoubang.html')

@app.route('/guangxizhiye')
def guangxizhiye():
    return render_template('guangxizhiye.html')

@app.route('/qianzhitong')
def qianzhitong():
    return render_template('qianzhitong.html')

@app.route('/xiquer')
def xiquer():
    return render_template('xiquer.html')

@app.route('/zhihuijiaofu')
def zhihuijiaofu():
    return render_template('zhihuijiaofu.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

# 启动应用前初始化数据库
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
