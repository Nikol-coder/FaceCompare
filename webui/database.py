from flask import Flask
import pymysql
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True, template_folder='templates')

# 配置数据库连接信息
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'username'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'database_name'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'facecp'

# 创建数据库连接
db = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)


# 创建数据库游标
cursor = db.cursor()


# 查询数据
@app.route('/')
def index():
    # 执行查询语句
    cursor.execute("SELECT * FROM usertable")
    result = cursor.fetchall()
    
    # 处理查询结果
    users = []
    for row in result:
        user = {
            'userid': row[0],
            'username': row[1],
            'password': row[2],
            'province': row[3],
            'tel': row[4]            
        }
        users.append(user)

    print(users)
 
    # 返回结果
    return render_template('login.html', users=users)

#插入数据
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    username = 'John'
    password = '4563'
    province = '河北'
    tel = 'john@example.com'

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 根据用户名和密码查询用户

    # 执行插入语句
    cursor.execute("INSERT INTO usertable (username, password, province, tel) VALUES (%s, %s, %s, %s)", (username, password, province, tel))
    
    # 提交事务
    db.commit()
    
    print('User created successfully')

    return render_template('login.html')

#更新数据
@app.route('/update_user')
def update_user():
    id = 1
    tel = 'jane@example.com'
    
    # 执行更新语句
    cursor.execute("UPDATE usertable SET tel = %s WHERE userid = %s", (tel, id))
    
    # 提交事务
    db.commit()
    
    return 'User updated successfully'

#删除数据
@app.route('/delete_user')
def delete_user():
    id = 1
    
    # 执行删除语句
    cursor.execute("DELETE FROM usertable WHERE userid = %s", (id,))
    
    # 提交事务
    db.commit()
    
    return 'User deleted successfully'



if __name__ == '__main__':
    app.run()
