from flask import Flask,request,render_template
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
mysql=MySQL()
app=Flask(__name__)
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='qwerty'
app.config['MYSQL_DB']='first'
app.config['MYSQL_HOST']='localhost'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False
app.config['MAIL_USERNAME']='b.s.karthikeyan26@gmail.com'
app.config['MAIL_PASSWORD']='valakr6_26'
app.config['MAIL_DEFAULT_SENDER']='b.s.karthikeyan26@gmail.com'
mail=Mail(app)
mysql.init_app(app)
@app.route('/')
def reg():
	return render_template("reg.html")
@app.route('/regcheck',methods=['POST','GET'])	
def rcheck():
	if request.method=='POST':
		email=request.form['email']
		password=request.form['psw']
		rpass=request.form['psw-repeat']
		if password==rpass:
			cursor=mysql.connection.cursor()
			cursor.execute("SELECT * from third")
			z=cursor.fetchall()
			for i in range(len(z)):
				if z[i][0]==email:
					return "email already exists go back and try with alternate email"
				
			cursor.execute("INSERT INTO third (email,password) VALUES (%s,%s)",(email,password))
			mysql.connection.commit()
			cursor.close()
			return render_template("log.html")
		else:
			return "Please go back and enter the password correctly"
	else:
		return "post error"	    
@app.route('/emailt',methods=['POST','GET'])
def e():
	if request.method=='POST':
		e=request.form['e']
		p=request.form['p']
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * from third")
		d=cursor.fetchall()
		cursor.close()
		for i in range(len(d)):
			if d[i][0]==e:
				if d[i][1]==p:
					msg=Message('hello',sender='b.s.karthikeyan26@gmail.com',recipients=[d[i][0]])
					mail.send(msg)
					return "mail sent"
				else:
					return "Incorrect password go back and try again"
		return "you have not registered"
@app.route('/r',methods=['POST','GET'])
def ind():
    if request.method=='POST':
    	return render_template("log.html")

@app.route('/forgot',methods=['POST'])
def resetpass():
	if request.method=='POST':
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from third into outfile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/student.csv' fields terminated by ',' lines terminated by '\n'")
		return "file ok"
@app.route('/forgot1',methods=['GET','POST'])
def reset():
	if request.method=='POST':
		re=request.form['e1']
		cur=mysql.connection.cursor()
		cur.execute("SELECT * from third")
		d=cur.fetchall()
		cur.close()
		for i in range(len(d)):
			if d[i][0]==re:
				pa=d[i][1]
				msg=Message('Password request',sender='b.s.karthikeyan26@gmail.com',recipients=[re])
				msg.html=render_template("msg.html",pw=pa)
				mail.send(msg)
				return "password sent via mail"
		return "you have not registered"

	
if __name__ == '__main__':
	app.run(debug=True) 			    


