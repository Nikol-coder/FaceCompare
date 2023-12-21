from hmac import new
import re
from flask import Flask, jsonify
import flask
from numpy import place
import pymysql
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Null
from mimacode import jiami, jiemi, chuli
import json
import os

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
            'pictureid': row[0],
            'name': row[2],
            'age': row[3],
            'province': row[4],
            'price': row[5]            
        }
        tasks.append(task)
    print(tasks)

    data_json = {"code": 0, "msg": "响应失败？", "count": len(tasks), "data": tasks}

    with open("./static/json/manager/demo1.json", "w", encoding='utf-8') as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
        f.close()
 
    # 返回结果
    return render_template('/Admin/user_Task.html')


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
            'place': row[2],
            'time': row[1].strftime('%Y-%m-%d'),
        }
        videos.append(video)
    print(videos)
    data_json = {"code": 0, "msg": "响应失败？", "count": len(videos), "data": videos}

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
            # 'password': row[2],
            'province': row[3],
            'tel': row[4]            
        }
        users.append(user)

    data_json = {"code": 0, "msg": "响应失败？", "count": len(users), "data": users}

    with open("./static/json/manager/demo1.json", "w", encoding='utf-8') as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
        f.close()

    print(users)
 
    # 返回结果
    return render_template('/Admin/user_manage.html')


# 悬赏管理
@app.route('/task_manage')
def task_manage():
    cursor.execute("SELECT * FROM pictable WHERE flag = 1")    # 待修改 flag 应有三种状态
    result = cursor.fetchall()
    # 处理查询结果
    tasks = []
    for row in result:
        task = {
            'pictureid': row[0],
            'name': row[2],
            'age': row[3],
            'province': row[4],
            'price': row[5]            
        }
        tasks.append(task)

    data_json = {"code": 0, "msg": "响应失败？", "count": len(tasks), "data": tasks}

    with open("./static/json/manager/demo1.json", "w", encoding='utf-8') as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
        f.close()
    print(tasks)
 
    # 返回结果
    return render_template('/Admin/task_manage.html')

# 删除视频      --- 视频管理
@app.route('/delete_video',methods=['GET','POST'])
def delete_video():
    pass

# 修改视频信息  --- 视频管理
@app.route('/modify_video',methods=['GET','POST'])
def modify_video():
    videoid = request.args.get('videoid')
    time = request.args.get('time')
    place = request.args.get('place')


    print("videoid: ", videoid)
    print("time: ", time)
    print("place: ", place)
    print("修改视频！！！")

    response_data = {
        'status': 'success',
        'message': '已修改悬赏'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response

# 获取视频   ---- 视频管理
@app.route('/get_video',methods=['GET','POST'])
def get_video():
    videoid = None
    if request.method == 'POST':
        videoid = request.form["videoid"]

    elif request.method == 'GET':
        videoid = request.args.get("videoid")

    if videoid is None:
        print("no videoid!!!!")
        print("获取图片！！！")
    else:
        print("videoid id: ", videoid)
        print("获取图片！！！")

    response_data = {
        'status': 'success',
        'videoUrl': '/static/video/'+ videoid + '.mp4'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response
 
# 通过悬赏   --- 审核悬赏过程 用户上传
@app.route('/permit_task',methods=['GET','POST'])
def permit_task():
    pictureid = None
    if request.method == 'POST':
        pictureid = request.form["pictureid"]

    elif request.method == 'GET':
        pictureid = request.args.get("pictureid")

    if pictureid is None:
        print("no pictureid!!!!")
    else:
        print(pictureid)
        print("通过悬赏！！！")
    
    response_data = {
        'status': 'success',
        'message': '审核已通过'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response
    

# 拒绝悬赏   ----审核悬赏过程 用户上传
@app.route('/deny_task',methods=['GET','POST'])
def deny_task():
    pictureid = None
    if request.method == 'POST':
        pictureid = request.form["pictureid"]

    elif request.method == 'GET':
        pictureid = request.args.get("pictureid")

    if pictureid is None:
        print("no pictureid!!!!")
    else:
        print(pictureid)
        print("拒绝悬赏！！！")

    response_data = {
        'status': 'success',
        'message': '已拒绝'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response

# 获取图片   ----审核/管理悬赏过程
@app.route('/get_image',methods=['GET','POST'])
def get_image():
    pictureid = None
    if request.method == 'POST':
        pictureid = request.form["pictureid"]

    elif request.method == 'GET':
        pictureid = request.args.get("pictureid")

    if pictureid is None:
        print("no pictureid!!!!")
        print("获取图片！！！")
    else:
        print("picture id: ", pictureid)
        print("获取图片！！！")

    response_data = {
        'status': 'success',
        'imageUrl': '/static/images/'+ pictureid + '.jpg'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response


# 删除悬赏   --- 管理悬赏过程
@app.route('/delete_reward',methods=['GET','POST'])
def delete_reward():
    pictureid = None
    if request.method == 'POST':
        pictureid = request.form["pictureid"]

    elif request.method == 'GET':
        pictureid = request.args.get("pictureid")

    if pictureid is None:
        print("no pictureid!!!!")
        print("删除悬赏！！！")
    else:
        print("picture id: ", pictureid)
        print("删除悬赏！！！")

    response_data = {
        'status': 'success',
        'message': '已删除'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response

# 修改悬赏   --- 管理悬赏过程
@app.route('/modify_reward',methods=['GET','POST'])
def modify_reward():
    pictureid = request.args.get('pictureid')
    name = request.args.get('name')
    age = request.args.get('age')
    province = request.args.get('province')
    price = request.args.get('price')


    print("pictureid: ", pictureid)
    print("name: ", name)
    print("age: ", age)
    print("province: ", province)
    print("price: ", price)
    print("修改悬赏！！！")
    response_data = {
        'status': 'success',
        'message': '已修改悬赏'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response

# 修改悬赏图片   --- 管理悬赏过程
@app.route('/modify_reward_picture',methods=['GET','POST'])
def modify_reward_picture():


    file = request.files['file']
    print("file: ", file)
    filename = file.filename
    print("filename: ", filename)
    file.save(os.path.join('static/images', filename))  # 保存文件
    print("修改悬赏图片！！！")
    response_data = {
        'status': 'success',
        'message': '已修改悬赏图片'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response



# 封禁   --- 管理用户
@app.route('/manager_delete_user', methods=['GET','POST'])
def manager_delete_user():
    userid = None
    if request.method == 'POST':
        userid = request.form["userid"]

    elif request.method == 'GET':
        userid = request.args.get("userid")

    if userid is None:
        print("no userid!!!!")
    else:
        print("userid: ", userid)
        print("删除用户 收到消息！！！")

    response_data = {
        'status': 'success',
        'message': '已封禁'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response


# 修改用户密码   --- 管理用户
@app.route('/change_password', methods=['GET','POST'])
def change_password():
    userid = None
    new_password = None
    if request.method == 'POST':
        userid = request.form["userid"]
        new_password = request.form["newpassword"]

    elif request.method == 'GET':
        userid = request.args.get("userid")
        new_password = request.args.get("newpassword")

    if userid is None:
        print("no userid!!!!")
        print("no new_password!!!!")
    else:
        print("userid: ", userid)
        print("newpassword:  ", new_password)
        print("修改密码！！！")

    response_data = {
        'status': 'success',
        'message': '密码已修改'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response




if __name__ == '__main__':
    app.run()

