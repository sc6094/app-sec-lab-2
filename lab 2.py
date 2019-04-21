from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='app sec',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to index function
@app.route('/')
def index():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #get info from html page
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    #SQLi vulnerability by executing SELECT * FROM user WHERE username = '[aa]' and password = '[anything' or '1' = '1]'
    cursor.execute("SELECT * FROM user WHERE username = '%s' and password = '%s'" % (username, password))

    data = cursor.fetchone()

    cursor.close()
    error = None
    if(data):
        #if data is found, log in is successful
        return redirect(url_for('home', username=username))
    else:
        #returns an error message to the html page
        error = 'Invalid username or password'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #get info from the html page
    username = request.form['username']
    password = request.form['password']

    
    cursor = conn.cursor()
    #executes query
    query = "SELECT * FROM user WHERE username = '%s'"
    cursor.execute(query % username)
  
    data = cursor.fetchone()
    
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = "INSERT INTO user VALUES('%s', '%s')"
        cursor.execute(ins % (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home/<username>')
#weak authenication 
# entering "http://localhost:5000/home/aa" will go straight to this page without the requirement of logging in 
def home(username):
    cursor = conn.cursor();
    query = 'SELECT * FROM account WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=username, accountinfo=data)

@app.route('/logout')
def logout():
    return redirect('/')
        
app.secret_key = 'some key'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)