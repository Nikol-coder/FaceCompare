from flask import Flask, jsonify
import pymysql
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from mimacode import jiami, jiemi, chuli
import json

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
app.config['MYSQL_DB'] = 'face'

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
    # 返回结果
    # return render_template('selectuser.html')
    return render_template('manager_login.html')
    # return render_template('.html')

#查询用户
@app.route('/search')
def search():
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
@app.route('/create_user', methods=['GET','POST'])
def create_user():

    if request.method == 'POST':
        # 结合createuser.html页面，创建用户
        userid = request.form.get("id")
        username = request.form.get("username") 
        password = request.form.get("pwd1") 
        province = request.form.get("pro") 
        tel = request.form.get("tel")
        password = jiami(password)
        print("加密代码：",password)
        password = str(password)
        # 执行插入语句
        cursor.execute("INSERT INTO usertable (userid,username, password, province, tel) VALUES (%s,%s, %s, %s, %s)", (userid,username, password, province, tel))
        jiemicode = jiemi(password)

        print("解密代码: ",jiemicode)
        # 提交事务
        db.commit()
        
        print('User created successfully')

        return render_template('login.html')
    else:
        return render_template('createuser.html')

#登录
@app.route('/login', methods=['GET','POST'])
#插入数据
def login():

    if request.method == 'POST':
        # 结合createuser.html页面，创建用户
        userid = request.form.get("username")
        password = request.form.get("password") 
        pwd = jiami(password)
        print("加密代码：",pwd)
        # 执行插入语句
            # 执行查询语句
        cursor.execute("SELECT * FROM usertable where userid = %s", (userid))
        result = cursor.fetchall()
        mima = result[0][2]
        jiemicode = jiemi(mima)

        print("\n解密代码: ",jiemicode)
        # 提交事务
        db.commit()
        password = chuli(password)
        if password == jiemicode:
            print('User login successfully')
            return render_template('selectuser.html')
        else:
            print('User login unsuccessfully')
            return render_template('login.html')

    else:
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
    return render_template('updateuser.html')

#删除数据
@app.route('/delete_user',methods=['GET','POST'])
def delete_user():
    if request.method == 'POST':
        id = request.form.get('id') 
        pwd = request.form.get('pwd')
        print(id)
        print(pwd)
        pwd = jiami(pwd)
        # 执行删除语句
        if pwd and pwd.strip():
            cursor.execute("DELETE FROM usertable WHERE userid = %s and password = %s", (id,pwd))
        
            # 提交事务
            db.commit()
            
            print('User deleted successfully')

            return render_template('login.html')
        else:
            print('User deleted unsuccessfully')
            return render_template('deleteuser.html')
    else:
        return render_template('deleteuser.html')


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
    with open("./static/json/manager/demo1.json", "w",encoding='utf-8') as f:
        for row in result:
            video = {
                'videoid': row[0],
                'place': row[2],
                'time': row[1].strftime('%Y-%m-%d'),
            }

            videos.append(video)
        data_json = {"code": 0, "msg": "响应失败？", "count": videos.count(), "data": videos}

    with open("./static/json/manager/demo1.json", "w", encoding='utf-8') as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
        f.close()

    # 返回结果
    return render_template('/Admin/manage_video.html')


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
    return render_template('/Admin/user_manage.html', users=users)


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

# 删除视频      --- 视频管理
@app.route('/delete_video',methods=['GET','POST'])
def delete_video():
    pass

# 修改视频信息  --- 视频管理
@app.route('/modify_video',methods=['GET','POST'])
def modify_video():
    pass

# 通过悬赏   --- 审核悬赏过程
@app.route('/permit_task',methods=['GET','POST'])
def permit_task():
    pass

# 拒绝悬赏   ----审核悬赏过程
@app.route('/deny_task',methods=['GET','POST'])
def deny_task():
    pass


# 删除悬赏   --- 管理悬赏过程
@app.route('/delete_reward',methods=['GET','POST'])
def delete_reward():
    pass

# 修改悬赏   --- 管理悬赏过程
@app.route('/modify_reward',methods=['GET','POST'])
def modify_reward():
    pass

# 封禁   --- 管理用户
@app.route('/blockade_user',methods=['GET','POST'])
def blockade_user():
    pass


# 修改用户密码   --- 管理用户
@app.route('/change_user_passwd',methods=['GET','POST'])
def change_user_passwd():
    pass

if __name__ == '__main__':
    app.run()

