from email.mime import image
from hmac import new
from operator import ne
import re
from sys import path
from tkinter import image_names
from flask import Flask, jsonify, url_for
import flask
from numpy import place
import pymysql
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Null
from mimacode import hash_password
import json
import os
import subprocess
from flask import send_file

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True, template_folder='templates')

# 配置数据库连接信息
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'username'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'database_name'
# app.config['MYSQL_HOST'] = '192.168.230.129'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'facecp'
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

tmp_name = None

# -------user behavior------------------------

# 查询数据
@app.route('/')
def index():
    # 返回结果
    # return render_template('selectuser.html')
    # return render_template('manager_login.html')
    return render_template('login.html')


@app.route('/modify_info', methods=['GET', 'POST'])
def modify_info():
    if request.method == 'POST':
        user_id = request.form.get('USERID')
        username = request.form.get('username')
        province = request.form.get('province')
        tel = request.form.get('tel')
        # 在这里更新数据库
        # 执行更新语句
        if not db.open:
            db.ping(reconnect=True)
        if tel and tel.strip() and username and username.strip() and province and province.strip():
            cursor.execute("UPDATE usertable SET tel = %s, username = %s, province = %s WHERE userid = %s", (tel, username, province, user_id))
            global tmp_name
            tmp_name = username
            # 提交事务
            db.commit()
            print('User updated successfully')
            return render_template('index.html',Username=tmp_name)
        else:
            print('User updated unsuccessfully')
            return render_template('modify_info.html',Username=tmp_name)
        
    else:
        # 从数据库中获取原有的信息
        user_id = request.args.get('userid')
        # 首先，检查用户是否存在
        print(user_id)
        if not db.open:
            db.ping(reconnect=True)
        cursor.execute("SELECT username, province, tel FROM usertable WHERE userid = %s", (user_id,))
        result = cursor.fetchall()
        for row in result:
            username = row[0]
            province = row[1]
            tel = row[2]
        # 提交事务
        db.commit()
        return render_template('modify_info.html', Username=username, Province=province, Tel=tel)


#上传图片
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        # 在这里处理图片
        # 指定保存位置
        # save_path = "C:/Users/10698/Desktop/ff/FaceCompare/face"
        # file_path = os.path.join(save_path, "uploaded_image.jpg")
        this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
        print("this_path: ",this_path)
        file_path = os.path.normpath(os.path.join(this_path, "../face/uploaded_image.jpg"))
        print("upload file_path: ", file_path)
        # 保存图片
        image.save(file_path)
        print(file_path)
        return jsonify({'message': '图片上传成功', 'image_url': file_path})
    else:
        return "No image in request", 400
    

#比较图片
@app.route('/compare', methods=['GET'])
def compare():
    this_path = os.path.dirname(os.path.abspath(__file__))
    print("this_path: ",this_path)
    subprocess.run(['python', 'demo.py'], cwd=os.path.normpath(os.path.join(this_path, "../face/InsightFace_Pytorch-master")))
    # image_names = os.listdir('C:/Users/10698/Desktop/ff/FaceCompare/webui/static/manzu/')
    print("this_path2: ",this_path)
    print("this_path_image: : ",os.path.normpath(os.path.join(this_path, "static/manzu/")))

    image_names = os.listdir(os.path.normpath(os.path.join(this_path, "static/manzu/")))
                 
    print(image_names)

    image_numbers = [name.split('.')[0] for name in image_names]

    print(image_numbers)

    # 创建一个字典来存储结果
    results = {}

    for tmp_img in image_numbers:
        if not db.open:
            db.ping(reconnect=True)
        query = """
        SELECT pictable.province, usertable.tel
        FROM pictable
        INNER JOIN usertable ON pictable.userid = usertable.userid
        WHERE pictable.picid = %s
        """
        cursor.execute(query, (tmp_img,))
        result = cursor.fetchall()

        # 将结果存储到字典中
        results[tmp_img] = result

    print(results)

    # 将结果转换为JSON格式并返回
    return jsonify(image_names=image_names, results=results)



#跳转到修改密码网页 /modify_mima
@app.route('/modify_mima')
def modify_mima():
    return render_template('modify_mima.html')

#跳转到主页 /index
@app.route('/index')
def index1():
    return render_template('index.html',Username=tmp_name)

#跳转到网页 /lookup
@app.route('/lookup')
def lookup():
    return render_template('lookup.html',Username=tmp_name)

# 跳转到网页 /createuser
@app.route('/createuser')
def createuser():
    return render_template('createuser.html')

#查看图片
@app.route('/api/images', methods=['GET'])
def get_images():
    if not db.open:
        db.ping(reconnect=True)
    cursor.execute("SELECT picid, name FROM pictable")
    data = cursor.fetchall()
    images = [{'url': "./static/images/"+str(int(url))+".jpg", 'alt': str(name)} for url, name in data]
    return jsonify(images)


#查看视频
@app.route('/api/videos', methods=['GET'])
def get_videos():
    if not db.open:
        db.ping(reconnect=True)
    cursor.execute("SELECT videoid FROM videotable")
    data = cursor.fetchall()
    videos = [{'url': "./static/video/"+str(int(url[0]))+".mp4"} for url in data]
    return jsonify(videos)

#修改用户密码
@app.route('/user_change_password', methods=['POST'])
def user_change_password():
    user_id = request.form.get('USERID')
    old_password = request.form.get('oldpwd')
    new_password = request.form.get('pwd1')
    request.form
    # 首先，检查用户是否存在
    cursor.execute("SELECT password FROM usertable WHERE userid = %s", (user_id,))
    result = cursor.fetchone()

    # 验证旧密码是否正确
    mima = result[0]
    print(mima)
    jiamicode = hash_password(old_password)

    print("\n加密代码: ",jiamicode)
    if mima == jiamicode:
        # 更新密码
        password = hash_password(new_password)
        cursor.execute("UPDATE usertable SET password = %s WHERE userid = %s", (password, user_id))
        db.commit()
        # 返回登录页
        return render_template('login.html', message='密码修改成功')
    else:
        print('User modify unsuccessfully')
        return render_template('login.html', message='密码修改失败')



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
        password = hash_password(password)
        print("加密代码：",password)
        password = str(password)
        # 执行插入语句
        cursor.execute("INSERT INTO usertable (userid,username, password, province, tel) VALUES (%s,%s, %s, %s, %s)", (userid,username, password, province, tel))

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
        print("userid :", userid)
        pwd = hash_password(password)
        print("加密代码：", pwd)
        # 执行插入语句
        # 执行查询语句
        if not db.open:
            db.ping(reconnect=True)
        cursor.execute("SELECT * FROM usertable where userid = %s", (userid))
        result = cursor.fetchall()
        print("result: ", result)
        if result == ():
            print("用户不存在")
            return render_template('login.html')
        mima = result[0][2]
        print("mima: ", mima)

        # 提交事务
        Username = result[0][1]
        global tmp_name
        tmp_name = Username
        db.commit()
        password = hash_password(password)
        if password == mima:
            print('User login successfully')
            return render_template('index.html', Username=tmp_name)
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
        pwd = hash_password(pwd)
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

# 用户登陆后界面
@app.route('/user_login')
def user_login():
    return render_template('index.html',Username=tmp_name)

@app.route('/reward_test')
def reward_test():
    return render_template('user_reward_manage.html')


# 用户悬赏管理界面
@app.route('/user_reward_manage/<int:user_id>')
def user_reward_manage(user_id):
    cursor.execute('SELECT * FROM pictable WHERE userid = %d' % user_id)
    results = cursor.fetchall()
    print(results)
    return render_template('user_reward_manage.html')

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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(this_path, "static/json/manager/demo1.json")
    with open(path_json, "w", encoding='utf-8') as f:
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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(this_path, "static/json/manager/demo1.json")
    with open(path_json, "w", encoding='utf-8') as f:
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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(this_path, "static/json/manager/demo1.json")
    with open(path_json, "w", encoding='utf-8') as f:
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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(this_path, "static/json/manager/demo1.json")
    with open(path_json, "w", encoding='utf-8') as f:
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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_json = os.path.join(this_path, "'static/video/'")

    video_path = path_json + videoid + '.mp4'
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
        this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
        path_video = os.path.join(this_path, "'static/video/'")
        video.save(os.path.join(path_video, filename))

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
        'imageUrl': '/static/test/'+ pictureid + '.jpg'
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
    this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    path_pic = os.path.join(this_path, "'static/test/'")

    picture_path = path_pic + pictureid + '.jpg'
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
        this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
        path_pic = os.path.join(this_path, "'static/test/'")
        picture.save(os.path.join(path_pic, filename))

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

    db_change_passwor(userid, hash_password(new_password))

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
    cursor.execute("UPDATE usertable SET password = %s WHERE userid = %s", (newpassword, userid))
    db.commit()

    return True


if __name__ == '__main__':
    app.run()
    # print(os.path.dirname(os.path.abspath(__file__)))