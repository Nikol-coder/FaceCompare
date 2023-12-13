from flask import Flask, jsonify
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
    return render_template('user.html', users=users)

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
@app.route('/update_user', methods=['POST'])
def update_user():
  id = request.form.get('id')
  tel = request.form.get('tel')

  # 执行更新语句
  if tel and tel.strip():
    cursor.execute("UPDATE usertable SET tel = %s WHERE userid = %s", (tel, id))

    # 提交事务
    db.commit()

    print('User updated successfully')

    return render_template('login.html')
  else:

    print('User updated unsuccessfully')
    return render_template('adduser.html')

#删除数据
@app.route('/delete_user')
def delete_user():
    id = 1
    
    # 执行删除语句
    cursor.execute("DELETE FROM usertable WHERE userid = %s", (id,))
    
    # 提交事务
    db.commit()
    
    return 'User deleted successfully'


# -------manager--------

# 返回未处理的任务
@app.route('/show_user_Task')
def show_user_Task():
    cursor.execute("SELECT * FROM pictable WHERE flag = 0")    # 待修改 flag 应有三种状态
    result = cursor.fetchall()
    # 处理查询结果
    tasks = []
    for row in result:
        task = {
            'picture': row[0],
            'name': row[2],
            'age': row[3],
            'province': row[4],
            'price': row[5]            
        }
    tasks.append(task)

    print(tasks)
 
    # 返回结果
    return render_template('/Admin/user_Task.html', tasks=tasks)


# 视频管理页面
@app.route('/manage_video')
def manage_video():
    cursor.execute("SELECT * FROM videotable") 
    result = cursor.fetchall()
    # 处理查询结果
    videos = []
    for row in result:
        video = {
            'videoid': row[0],
            'place': row[1],
            'time': row[2],
          
        }
    videos.append(video)

    print(videos)
 
    # 返回结果
    return render_template('/Admin/manage_video.html', videos=videos)


# 用户管理
@app.route('/user_manage')
def user_manage():
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
    return render_template('user_manage.html', users=users)


# 悬赏管理
@app.route('/task_manage')
def task_manage():
    cursor.execute("SELECT * FROM pictable WHERE flag = 1")    # 待修改 flag 应有三种状态
    result = cursor.fetchall()
    # 处理查询结果
    tasks = []
    for row in result:
        task = {
            'picture': row[0],
            'name': row[2],
            'age': row[3],
            'province': row[4],
            'price': row[5]            
        }
    tasks.append(task)

    print(tasks)
 
    # 返回结果
    return render_template('/Admin/task_manage.html', tasks=tasks)



if __name__ == '__main__':
    app.run()
