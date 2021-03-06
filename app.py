#-*- coding:utf-8 -*-
from flask import Flask, render_template, request,flash
from flask_wtf.form import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
#配置数据库地址
#app.config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:123456@sharlench'
#动态追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'CQUPT'

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    password2 = PasswordField('确认密码',validators=[DataRequired(), EqualTo('password', '密码不一致')])
    submit = SubmitField('提交')
#与sql中相同
class supplier(db.Model):
    supplierNum = db.Column(db.VARCHAR(20), primary_key=True)
    supplierName = db.Column(db.VARCHAR(10))
    supplierdress = db.Column(db.VARCHAR(10))

@app.route('/dex')
def dex():
    return render_template('dex.html')

@app.route('/introduce')
def introduce():
    return 'this is SharlenChance'

@app.route('/change',methods=['GET','POST'])
def change():
    loginforms = LoginForm()
    if request.method == 'POST':
        oldname = request.form.get('oldname')
        olddate = request.form.get('olddate')
        oldcolor = request.form.get('oldcolor')
        newname = request.form.get('newname')
        newdate = request.form.get('newdate')
        newcolor = request.form.get('newcolor')
        if not all([oldname,olddate,oldcolor,newname,newdate,newcolor]):
            flash('数据不够，无法修改')
        else:
            store1 = supplier.query.filter_by(supplierName=oldname, supplierNum=olddate, supplierdress=oldcolor).first()
            store1.supplierName = newname
            store1.supplierNum = newdate
            store1.supplierdress = newcolor
            db.session.commit()
            return 'success'
    return render_template('change.html',form = loginforms)

@app.route('/delete',methods=['GET','POST'])
def delete():
    loginforms = LoginForm()
    if request.method == 'POST':
        supplierName = request.form.get('username')
        supplierNum = request.form.get('password')
        supplierdress = request.form.get('password2')
        if not all([supplierName,supplierNum,supplierdress]):
            flash('输入的信息不够，无法删除')
        else:
            store1 = supplier.query.filter_by(supplierName=supplierName,supplierNum=supplierNum,supplierdress=supplierdress).first()
            db.session.delete(store1)
            db.session.commit()
            return'success'
    return render_template('delete.html', form = loginforms)

@app.route('/search', methods=['GET','POST'])
def search():
    loginforms = LoginForm()
    if request.method == 'POST':
        shoename = request.form.get('shoename')
        data = request.form.get('data')
        color = request.form.get('color')
        if not all([shoename,data,color]):
            flash('输入的信息不够，无法查询')
        else:
            shoe1 = supplier.query.filter_by(supplierName=shoename, supplierNum=data, supplierdress=color).first()
            return render_template('elements.html',form = loginforms,shoe1 = shoe1)
    return render_template('generic.html',form = loginforms)

@app.route('/search3', methods=['GET','POST'])
def search3():
    loginforms = LoginForm()
    shoe3 = supplier.query.all()
    if request.method == 'POST':
        supplierName = request.form.get('username')
        output = []
        for record in shoe3:
            r_data = {}
            if record.supplierName == supplierName:
                r_data['shoeName'] = record.supplierName
                r_data['data'] = record.supplierNum
                r_data['color'] = record.supplierdress
                output.append(r_data)
        return render_template('success.html',form = loginforms,output = output)
    return render_template('success2.html',form = loginforms)

@app.route('/display', methods=['GET'])
def get_data2():
    myData = supplier.query.all()
    output = []
    for record in myData:
        r_data = {}
        r_data['supplierdress'] = record.supplierdress
        r_data['supplierNum'] = record.supplierNum
        r_data['supplierName'] = record.supplierName
        output.append(r_data)
    return render_template('testlist.html', myData = myData)

@app.route('/', methods = ['GET','POST'])
def index():
    loginforms = LoginForm()
    return render_template('dex.html',form = loginforms)

@app.route('/insert', methods =['GET','POST'])
def insert():
    loginforms = LoginForm()
    shoe1 = supplier()
    if request.method == 'POST':
        shoe1.supplierName = request.form.get('shoename')
        shoe1.supplierNum = request.form.get('data')
        shoe1.supplierdress = request.form.get('color')
        db.session.add(shoe1)
        db.session.commit()
        return '添加成功'
    return render_template('tax.html', form=loginforms)

if __name__ == '__main__':
    app.run()
