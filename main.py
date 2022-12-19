from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import Flask,request,make_response,abort

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'filesystem'
dsn = 'mysql+pymysql://root:peter63674782@127.0.0.1:3306/project7'
app.config['SQLALCHEMY_DATABASE_URI'] = dsn

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    sclass = db.Column(db.String(20))
    sex = db.Column(db.Integer)
    score = db.Column(db.Integer)
    def __init__(self,name,sclass,sex,score):
        self.name = name
        self.sclass = sclass
        self.sex = sex
        self.score = score


@app.route('/',methods=['GET','POST'])
def index():
    name = request.form['name']
    sclass = request.form['sclass']
    query_data = Student.query.filter(or_(Student.name == name , Student.sclass == sclass)).first()
    if request.method == 'POST':
        if not name or not sclass :
            return 'please enter all information'
        elif name == 'admin' and sclass == 'admin_sclass':
            resp = make_response('succcess_login')
            resp.set_cookie('name', name, max_age=3600)
            data = Student.query.all()
            d = ""
            for i in data:
                d += f"\n{i.name},{i.sclass},{i.sex},{i.score}\n"
            return d
        elif not query_data:
            abort(401)
            return 'wrong name or wrong sclass'
        else:
            resp = make_response('succcess_login')
            resp.set_cookie('name',name,max_age=3600)
            return f"hello {name},{resp}"


@app.route('/insert',methods=['GET','POST'])
def insert():
    name = request.form['name']
    sclass = request.form['sclass']
    sex = request.form['sex']
    score = request.form['score']
    cookie = request.cookies.get('name')
    if request.method == 'POST':
        student = Student(name,sclass,sex,score)
        db.session.add(student)
        db.session.commit()
        return 'success'


@app.route('/update',methods=['GET','POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    sclass = request.form['sclass']
    sex = request.form['sex']
    score = request.form['score']
    cookie = request.cookies.get('name')
    if request.method == 'POST':
        if not cookie:
            abort(401)
        else:
            Student.query.filter(Student.id == id).update({'name':name,'sclass':sclass,'sex':sex,'score':score})
            db.session.commit()
            return f'success update id:{id}'

@app.route('/delete',methods=['GET','POST'])
def delete():
    id = request.form['id']
    cookie = request.cookies.get('name')
    if request.method == 'POST':
        if not cookie:
            abort(401)
        else:
            Student.query.filter(Student.id==id).delete()
            db.session.commit()
            return f'success delete id:{id}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)