from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy,render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    # 获取所有用户
    users = User.query.all()
    print(users)
    return render_template('user.html', users=users)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 根据用户名和密码查询用户
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return 'Login success'
        else:
            return 'Login failed'
    return render_template('login.html')
