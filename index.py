#coding=utf8

from flask import Flask,redirect,url_for,render_template,request,jsonify,Blueprint
import jieba,re,math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io,base64
from wordcloud import WordCloud
import os,time
import lianjieshujuku
from shengchengMD5 import sheng_md5
from zhanghaomimalibiao import zhmmlist
from flask_login import login_required,login_user,current_user
from wsgiref.simple_server import make_server

app=Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')
# app=Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')

#进入分词页面
@app.route('/login',methods=['GET','POST'])
def login():
    method=request.method
    print(method)
    if method=="GET":
        return render_template('login.html')
    else:
        user_dict=request.form.to_dict()
        print(user_dict)
        username_list=zhmmlist()[0]
        userpwd_list=zhmmlist()[1]
        print(userpwd_list)
        print(username_list)
        if user_dict['username'] in username_list:
            index=username_list.index(user_dict['username'])
            print(index)
            if user_dict['userpwd'] == userpwd_list[index]:
                username=user_dict["username"]
                userpwd=user_dict["userpwd"]
                sql=f'select * from user where username="{username}" and userpwd="{userpwd}"'
                # id=lianjieshujuku.shujuku(sql)[0]['id']
                user=lianjieshujuku.shujuku(sql)
                print(user)
                data = {
                    'code': 200,
                    'msg': '登录成功',
                    'username':user_dict['username']
                }
                print('成功')
                login_user(user,force=True)
                fenci_dict = {'': ''}
                return render_template('index.html', data=fenci_dict)
            else:
                data = {
                    'code': 402,
                    'msg': '密码不正确',
                }
                return jsonify(data)
        else:
            data = {
                'code': 403,
                'msg': '无此用户',
            }
            return jsonify(data)


@app.route('/register',methods=['GET','POST'])
def register():
    method=request.method
    if method=="GET":
        return render_template('register.html')
    else:
        user_dict=request.form.to_dict()
        #生成md5唯一值
        username=user_dict['username']
        userpwd=user_dict['userpwd']
        usertime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        userrandom=np.random.randint(1,10000)
        usermd5=sheng_md5(str(username+userpwd+str(usertime)+str(userrandom)))
        #判断是否重复
        username_list=zhmmlist()[0]
        if username in username_list:
            data={
                'code':401,
                'msg':'用户名重复'
            }
            return jsonify(data)
        else:
            sql=f'insert into user(username,userpwd,registerdate,unionid) values("{username}","{userpwd}","{usertime}","{usermd5}")'
            lianjieshujuku.shujuku(sql=sql)
            data={
                'code':200,
                'msg':'注册成功'
            }
            return jsonify(data)

@app.route('/')
def fenci():
    url=request.url
    print(url)
    fenci_dict={'':''}
    return render_template('index.html',data=fenci_dict)


@app.route('/index')
def fenci_index():
    fenci_dict={'':''}
    return render_template('index.html',data=fenci_dict)

def heimingdan():
   hei_text =open('./hei_text.txt' ,'r' ,encoding='utf8' ,errors='ignore').readlines()
   hei_text=[i.strip() for i in hei_text]
   return hei_text

@app.route('/zhuanhua')
def zhuanhuaye():
    fenci_dict = {'': ''}
    print('zhuanhuazhuanhuazhuanhuazhuanhuazhuanhua')
    return render_template('index.html',data=fenci_dict)

@app.route('/jilu')
def jiluyemian():
    sql='select * from fenci'
    data1=lianjieshujuku.shujuku(sql)

    print('jilujilujilujilu')
    fenci_dict = {'': ''}
    return render_template('index.html',data=fenci_dict,sql_data=data1)

@app.route('/shanchujilu/<int:id>')
def shanchujilu(id):
    sql=f'delete from fenci where id={id}'
    lianjieshujuku.shujuku(sql=sql)
    fenci_dict = {'': ''}
    return '<script>alert("删除成功");window.location.href="/jilu"</script>'

@app.route('/wode')
def wodeyemian():
    fenci_dict = {'': ''}
    print('wodewodewodewodewodewodewode')
    return render_template('index.html',data=fenci_dict)

@app.route('/zhuanhua',methods=['POST'])
def zhuanhua():
    data=request.form.to_dict()
    txt=data['init_data']
    if txt == "":
        return "<script>alert('数据为空，请输入文本');window.location.href='/'</script>"
    pat="[\u4e00-\u9fa5a-zA-Z0-9]+"
    jieba.add_word('还钱')
    # 黑名单
    hei_text =heimingdan()
    txt=re.findall(pat,txt,re.S)
    txt=''.join(txt)
    outdir=''
    for word in txt:
        if word not in hei_text:
            outdir+=word
    sql_outdir=outdir[1:6]+'......'
    searchs=jieba.lcut(outdir,cut_all=True)
    fenci_dict={}
    for text in searchs:
        fenci_dict[text]=searchs.count(text)
    #获取词频前三个词
    cipin=sorted([(k,v) for k,v in fenci_dict.items()],key=lambda x:x[1],reverse=True)
    qiansan=cipin[0:3]
    w=WordCloud(font_path='./static/simhei.ttf',background_color='white')
    ciyu=w.generate_from_frequencies(fenci_dict)
    if os.path.exists("./static/img/fenci1.png"):
        os.remove('./static/img/fenci1.png')
    plt.imshow(ciyu)
    plt.axis('off')
    ciyu.to_file('./static/img/fenci1.png')
    sql_qiansan=str(qiansan)
    sql_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    sql=f'insert into fenci(fenciciyu,cipinqiansan,date) values("{sql_outdir}","{sql_qiansan}","{sql_date}")'
    lianjieshujuku.shujuku(sql)
    return render_template('index.html',data=fenci_dict,img='../static/img/fenci1.png',data1=qiansan)


if __name__ == '__main__':
    app.run(host='localhost',port=8888,debug=True)
    # server = make_server('172.22.106.178',5050, app)
    # server.serve_forever()



