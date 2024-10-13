from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title='首页')

# Other routes can be added here for different pages

if __name__ == '__main__':
    app.run(debug=True)
