from flask import Flask
from flask import render_template,request,redirect,url_for
from flask import flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from flask_login import current_user
from werkzeug.security import generate_password_hash

from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///knowledge.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

class User(db.Model,UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    first_name = db.Column(db.String(30),nullable=True)
    last_name = db.Column(db.String(30),nullable=False)
    administrator_flg = db.Column(db.Boolean,nullable=False,default=False)
    update_user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    update_at = db.Column(db.DateTime,default=datetime.now)
    update_number = db.Column(db.Integer,nullable=False)
    del_flg = db.Column(db.Boolean,default=False,nullable=False)
    #override(デフォルト,usermixinに定義されたget_idはidを呼び出すから)
    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

class Channel(db.Model):
    __tablename__ = "channel"
    channel_id = db.Column(db.Integer,primary_key=True)
    channel_name = db.Column(db.String(30),unique=True,nullable=False)
    overview = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    update_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    update_number = db.Column(db.Integer,nullable=False)

    #relationship
    knowledges = db.relationship("Knowledge",back_populates="channel")


class Knowledge(db.Model):
    __tablename__ = "knowledge"
    knowledge_id = db.Column(db.Integer,primary_key=True)
    knowledge = db.Column(db.String(255),nullable=False)
    channel_id = db.Column(db.Integer,db.ForeignKey('channel.channel_id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    update_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    update_number = db.Column(db.Integer,nullable=False)
    
    #relationship
    channel = db.relationship("Channel",back_populates="knowledges")


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
  if current_user.is_authenticated:
    channels = Channel.query.all()
    return render_template("index.html",channels = channels,title="チャンネル一覧")
  else:
    return redirect("/login")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email, password = password).first()
        if user:
            #ログイン成功の際に、自動的にユーザ情報をロードする
            login_user(user)
            if password == "knowledge123":
                return redirect("/changePassword")
            else:
                return redirect("/")
        else:
            errormessage = "メールアドレスまたはパスワードが間違っています"
            return render_template("login.html",errormessage = errormessage)
    else:
        return render_template('login.html',errormessage = "")
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")

@app.route('/createChannel',methods=['POST','GET'])
@login_required
def createChannel():
    if request.method == 'POST':
        channel_name = request.form.get('channel_name')
        overview = request.form.get('overview')
        channel = Channel.query.filter_by(channel_name = channel_name).first()
        if channel :
            errormessage = "チャンネル「"+channel_name+"」は既に存在します"
            return render_template("createChannel.html",errormessage=errormessage,title="チャンネル登録")
        else:
            channel = Channel(channel_name=channel_name,overview=overview,user_id = current_user.user_id,update_at=datetime.now(),update_number=1)
            db.session.add(channel)
            db.session.commit()
            return redirect("/")
    else:
        return render_template("createChannel.html",errormessage="",title="チャンネル登録")
    
@app.route('/editChannel/channel_id=<int:channel_id>',methods=['POST','GET'])
@login_required
def editChannel(channel_id):
    if request.method == 'POST':
        channel_name = request.form.get('channel_name')
        overview = request.form.get('overview')
        channel = Channel.query.get(channel_id)
        check_channelName= Channel.query.filter((Channel.channel_name == channel_name) & (Channel.channel_name != channel.channel_name)).first()
        if check_channelName :
            errormessage = "チャンネル「"+channel_name+"」は既に存在します"
            return render_template("editChannel.html",errormessage=errormessage,title="チャンネル編集",channel=channel)
        else:
            channel.channel_name = channel_name
            channel.overview = overview
            channel.update_at = datetime.now()
            channel.update_number += 1
            db.session.commit()
            return redirect("/")
    else:
        channel = Channel.query.get(channel_id)
        return render_template("editChannel.html",errormessage="",title="チャンネル編集",channel=channel)
    
@app.route('/deleteChannel/channel_id=<int:channel_id>')
@login_required
def deleteChannel(channel_id):
    channel = Channel.query.get(channel_id)
    knowledges = Knowledge.query.filter_by(channel_id = channel_id).all()
    for knowledge in knowledges:
        db.session.delete(knowledge)
    db.session.delete(channel)
    db.session.commit()
    return redirect("/")

@app.route("/listKnowledge/channel_id=<int:channel_id>")
def listKnowledge(channel_id):
    knowledges = Knowledge.query.filter_by(channel_id=channel_id).all()
    return render_template("listKnowledge.html",knowledges=knowledges,title="ナレッジ一覧")

@app.route("/createKnowledge",methods=['POST','GET'])
@login_required
def createKnowledge():
    if request.method == "POST":
        channel_id = request.form.get('channel_id')
        knowledge = request.form.get('knowledge')
        knowledge = Knowledge(knowledge = knowledge,channel_id = channel_id,user_id = current_user.user_id,update_at = datetime.now(),update_number=1)
        db.session.add(knowledge)
        db.session.commit()
        return redirect(url_for('listKnowledge',channel_id=channel_id))
    else:
        channels = Channel.query.all()
        return render_template("createKnowledge.html",title="ナレッジ追加",errormessage="",channels=channels)
    
@app.route("/editKnowledge/knowledge_id=<int:knowledge_id>",methods=['POST','GET'])
@login_required
def editKnowledge(knowledge_id):
    if request.method == "POST":
        channel_id = request.form.get('channel_id')
        knowledge = request.form.get('knowledge')
        knowledge_obj= Knowledge.query.get(knowledge_id)
        knowledge_obj.knowledge = knowledge
        knowledge_obj.channel_id = channel_id 
        knowledge_obj.update_at = datetime.now()
        knowledge_obj.update_number += 1
        db.session.commit()
        return redirect(url_for('listKnowledge',channel_id = channel_id))
    else:
        knowledge = Knowledge.query.get(knowledge_id)
        channels = Channel.query.all()
        return render_template("editKnowledge.html",knowledge = knowledge, channels = channels ,title="ナレッジ編集",errormessage="")
    
@app.route("/deleteKnowledge/channel_id=<int:channel_id>/knowledge_id=<int:knowledge_id>")
@login_required
def deleteKnowledge(knowledge_id,channel_id):
    knowledge = Knowledge.query.get(knowledge_id)
    db.session.delete(knowledge)
    db.session.commit()
    return redirect(url_for('listKnowledge',channel_id = channel_id))


@app.route("/searchKnowledge")
def searchKnowledge():
    keyword_str = request.args.get('keyword_str')
    keyword_list = keyword_str.split()
    knowledge_list = []
    knowledges = Knowledge.query.all()
    for knowledge in knowledges :
        if all(keyword.lower() in knowledge.knowledge.lower() for keyword in keyword_list):
            knowledge_list.append(knowledge)
    if len(knowledge_list) == 0 :
        errormessage = "検索キーワードに該当するナレッジありません"
    else:
        errormessage = ""
    return render_template("searchKnowledge.html",knowledges=knowledge_list,keyword_str=keyword_str,title="ナレッジ一覧",errormessage=errormessage)

@app.route("/userManager")
@login_required
def userManager():
    messages = get_flashed_messages(with_categories=True)
    users = User.query.filter_by(del_flg = False).all()
    return render_template("userManager.html",users=users,title="ユーザ管理",messages=messages)

@app.route("/createUser",methods=['POST'])
@login_required
def createUser():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    administrator_flg = True if request.form.get('administrator_flg') == "on" else False
    check_email = User.query.filter_by(email = email).first()
    if check_email != None :
        flash('入力したメールアドレスは既に存在します','errormessage')
        return redirect('/userManager')
    else:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    administrator_flg=administrator_flg,
                    password="knowledge123",
                    update_user_id=current_user.user_id,
                    update_at=datetime.now(),
                    update_number=1,
                    del_flg=False)
        db.session.add(user)
        db.session.commit()
        return redirect('/userManager')
    
@app.route("/deleteUser/user_id=<int:user_id>")
@login_required
def deleteUser(user_id):
    user = User.query.get(user_id)
    user.del_flg = True
    db.session.commit()
    flash("削除しました","success")
    return redirect('/userManager')

@app.route("/changePassword",methods=['POST','GET'])
@login_required
def changePassword():
    if request.method == "POST":
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            flash("新しいパスワードと確認用のパスワードが一致しない","errormessage")
            return redirect("/changePassword")     
        else:
            user = User.query.get(current_user.user_id)
            user.password = new_password
            db.session.commit()
            return redirect("/")     
    else:
        messages = get_flashed_messages(with_categories=True)
        return render_template('changePassword.html',title="パスワード変更",messages=messages)

@app.route("/resetPassword/user_id=<int:user_id>")
@login_required
def resetPassword(user_id):
    user = User.query.get(user_id)
    user.password = "knowledge123"
    db.session.commit()
    flash("パスワードを初期化しました！","success")
    return redirect("/userManager")

@app.route("/editUser/user_id=<int:user_id>",methods=['POST'])
@login_required
def editUser(user_id):
    if request.method == "POST":
        index = request.form.get('index')
        email = request.form.get('email'+index)
        first_name = request.form.get('first_name'+index)
        last_name = request.form.get('last_name'+index)
        administrator_flg = True if request.form.get('administrator_flg'+index) == "on" else False
        user = User.query.get(user_id)
        check_email = User.query.filter((User.email != user.email) & (User.email == email)).first()
        print("user_id"+str(user_id))
        if check_email:
            flash("入力したメールアドレスが既に存在します","errormessage")
            return redirect("/userManager")
        else:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.administrator_flg = administrator_flg
            db.session.commit()
            flash("ユーザー情報が更新されました","success")
            return redirect("/userManager")



