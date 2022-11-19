from flask import *
from flask_mysqldb import MySQL
import yaml,re 
import MySQLdb.cursors
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------
db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']

MySQL = MySQL(app)

@app.route('/',methods =['GET','POST'])
def hello_world():
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		userDetails = request.form
		email = userDetails['email']
		password = userDetails['password']
		comm = MySQL.connection.cursor()
		comm.execute("""select Password from cred where email = '%s'"""%(email))
		hash = comm.fetchone()
		user = pbkdf2_sha256.verify(password, hash[0])
		print(user)
		if user == True:
			pass
		# cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM cred Where email = %s and password = %s',(email,user))
		# accounts = cursor.fetchone()
		# if accounts:
		# 	session['loggedin'] = True
		# 	session['email'] = accounts['email']
		# 	session['name'] = accounts['name']
		# 	return "Welcome"
	return render_template("index.html")

@app.route("/register",methods =['GET','POST'])
def register():
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		userDetails = request.form
		name = userDetails["name"]
		email = userDetails["email"]
		password = userDetails['password']
		hashs = pbkdf2_sha256.hash(password)
		con = MySQL.connection.cursor()
		value = con.execute("""select * from cred where email = '%s'"""%(email))
		if len(password) < 8:
			flash("Password Should have atlest 8 char")
		elif re.search('[0-9]',password) is None:
			flash("Make sure you have Any One Numeric Value in password")
		elif re.search('[A-Z]',password) is None:
			flash("Make Sure you have One Capital letter in your password")
		elif re.match('[_@$]',password):
			flash("Make sure you have One Special Character in your password")
		elif value >= 1:
			flash("This Email already exist!")
			return redirect("/")
		else:
			try:
				con = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
				con.execute("insert into cred(name,email,password) value(%s, %s,%s)",(name,email,hashs))
				MySQL.connection.commit()
				flash("Succesfully Created Your Account")
				return redirect("/")
			except:
				flash("Ohhh ho! Something Went Wrong...")
				return redirect("/register")
	return render_template("register.html")


if __name__ == '__main__':
	app.run(debug=True)
