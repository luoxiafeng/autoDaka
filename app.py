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

# 初始化数据库
def init_db():
    conn = sqlite3.connect('user_auth.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    # 插入管理员账号
    cursor.execute('SELECT * FROM users WHERE username=?', ('admin',))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
                       ('admin', 'admin456@@', '管理员'))
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

# 启动应用前初始化数据库
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
