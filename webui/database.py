from hmac import new
from operator import ne
import re
from flask import Flask, jsonify, url_for
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
app.config['MYSQL_HOST'] = '192.168.230.129'
# app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'face'
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
    # 返回结果
    # return render_template('selectuser.html')
    # return render_template('manager_login.html')
    return render_template('login.html')

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


# -------user behavior------------------------
#             cqh

# 用户操作页面
@app.route('/user_detail')
def user_detail():
    return render_template('user_detail')

# 用户进行悬赏
@app.route('/user_add_reward')
def user_add_reward():
    return render_template('user_add_reward.html')

# 用户查看悬赏
@app.route('/user_show_reward')
def user_show_reward():
    return render_template('user_show_reward.html')

# 用户删除悬赏
@app.route('/user_delete_reward')
def user_delete_reward():
    return render_template('user_delete_reward.html')


# -------manager--------
#    jxl
# -------manager--------
#   管理员管理任务部分
# -------manager--------
    
# 管理员登陆
@app.route('/login_manager', methods=['GET','POST'])
def login_manager():
    
    userid = request.form["username"]
    password = request.form["password"]
    cursor.execute("SELECT * FROM admintable where adminid = %s", (userid))
    result = cursor.fetchall()
    mima = result[0][1]
    print("userid: ", userid)
    print("password: ", password)
    print("mima: ", mima)
    # print("url", render_template("manager_login.html"))
    # 提交事务
    if password == mima:
        response_data = {
            'status': 'success',
            'success':True,
            'message': 'manager登录成功',
            'redirectUrl': url_for('manager_login')
            # 'content': render_template("manager_login.html")
        }
        response = flask.make_response(jsonify(response_data))
        response.status_code = 200
        return response

    else:
        response_data = {
            'status': 'success',
            'success':False,
            'message': 'manager登录失败',
            'redirectUrl': url_for('login.html')
            # 'content': render_template("login.html")
        }
        response = flask.make_response(jsonify(response_data))
        response.status_code = 200
        return response

# 管理员登陆成功后跳转到管理员界面
@app.route('/manager_login')
def manager_login():
    return render_template('manager_login.html')
    
    
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
    videoid = None
    if request.method == 'POST':
        videoid = request.form["videoid"]

    elif request.method == 'GET':
        videoid = request.args.get("videoid")

    if videoid is None:
        print("no videoid!!!!")
        print("删除悬赏！！！")
    else:
        print("video id: ", videoid)
        print("删除悬赏！！！")
    
    db_delete_video(videoid)

    video_path = '/static/video/' + videoid + '.mp4'
    if os.path.exists(video_path):
        os.remove(video_path)
    else:
        print("The file does not exist: ", video_path)

    response_data = {
        'status': 'success',
        'message': '已删除视频'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response

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

    db_modify_video(videoid, time, place)

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

# 上传视频   ---- 视频管理
@app.route('/upload_video', methods=['POST'])
def upload_video():
    place = request.form['place']
    time = request.form['time']
    video = request.files['video']

    print("place: ", place)
    print("time: ", time)   
    
    videoid = db_upload_video(place, time, video)

    if videoid is not None:
        print("videoid: ", videoid)
        filename = videoid + '.mp4'
        video.save(os.path.join('/static/video/', filename))

    # 保存地点和时间到数据库
    # ...

    response_data = {
        'status': 'success',
        'message': '视频已上传'
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

    db_permit_task(pictureid)
    
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

    db_deny_task(pictureid)

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

    db_delete_reward(pictureid)

    picture_path = '/static/images/' + pictureid + '.jpg'
    if os.path.exists(picture_path):
        os.remove(picture_path)
    else:
        print("The file does not exist: ", picture_path)

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

    pictureid = request.form['pictureid']
    name = request.form['name']
    age = request.form['age']
    province = request.form['province']
    price = request.form['price']
    
    print("pictureid: ", pictureid)
    print("name: ", name)
    print("age: ", age)
    print("province: ", province)
    print("price: ", price)
    print("修改悬赏！！！")


    db_modify_reward(pictureid, name, age, province, price)

    # 检查是否上传了图片
    if 'picture' in request.files:
        picture = request.files['picture']
        print("picture: ", picture)
        filename = pictureid + '.jpg'
        picture.save(os.path.join('/static/images/', filename))

    response_data = {
        'status': 'success',
        'message': '已修改悬赏'
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
    
    db_manager_delete_user(userid)

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

    db_change_passwor(userid, new_password)

    response_data = {
        'status': 'success',
        'message': '密码已修改'
    }
    response = flask.make_response(jsonify(response_data))
    response.status_code = 200
    return response


# --------- manager db----------
#    jxl
# --------- manager db----------
#   管理员管理任务的数据库部分
# --------- manager db----------

# 删除数据库视频
def db_delete_video(videoid):
    print("db delete video: ", videoid)
    cursor.execute("DELETE FROM videotable WHERE videoid = %s", (videoid))
    db.commit()
    return True

# 修改数据库视频
def db_modify_video(videoid, time, place):
    print("db modify video: ", videoid)
    print("db time: ", time)
    print("db place: ", place)
    cursor.execute("UPDATE videotable SET time = %s, place = %s WHERE videoid = %s", (time, place, videoid))
    db.commit()
    return True

# 上传数据库视频
def db_upload_video(place, time, video):
    print("db place: ", place)
    print("db time: ", time)
    # print("video: ", video)
    cursor.execute("INSERT INTO videotable (place, time) VALUES (%s, %s)", (place, time))
    db.commit()
    videoid = str(cursor.lastrowid)
    print("new instert video id : ", videoid)

    return videoid     # 返回视频id

# 通过悬赏    #  flag = 1
def db_permit_task(pictureid):
    print("pictureid:", pictureid)
    cursor.execute("UPDATE pictable SET flag = 1 WHERE pictureid = %s", (pictureid))
    db.commit()
    return True

# 拒绝悬赏    # flag = 2
def db_deny_task(pictureid):
    print("pictureid:", pictureid)
    cursor.execute("UPDATE pictable SET flag = 2 WHERE pictureid = %s", (pictureid))
    db.commit()
    return True

# 删除悬赏
def db_delete_reward(pictureid):
    print("pictureid:", pictureid)
    cursor.execute("DELETE FROM pictable WHERE pictureid = %s", (pictureid))
    db.commit()
    return True

# 修改悬赏
def db_modify_reward(pictureid, name, age, province, price):
    print("pictureid: ", pictureid)
    print("name: ", name)
    print("age: ", age)
    print("province: ", province)
    print("price: ", price)
    cursor.execute("UPDATE pictable SET name = %s, age = %s, province = %s, price = %s WHERE pictureid = %s", (name, age, province, price, pictureid))
    db.commit()
    return True

# 封禁用户
def db_manager_delete_user(userid):
    print("userid: ", userid)
    cursor.execute("DELETE FROM usertable WHERE userid = %s", (userid))
    db.commit()
    return True

# 修改用户密码
def db_change_passwor(userid, newpassword):
    print("userid: ", userid)
    print("newpassword:  ", newpassword)
    newpassword = jiami(newpassword)
    cursor.execute("UPDATE usertable SET password = %s WHERE userid = %s", (newpassword, userid))
    db.commit()

    return True


if __name__ == '__main__':
    app.run()

