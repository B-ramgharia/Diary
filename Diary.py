from flask import Flask, render_template, request 



app = Flask(__name__)





@app.route('/', methods=['GET', 'POST'])
def index():    return render_template('index.html')

@app.route('/HOME')
def HOME():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/Lock in Vault')
def lock_in_vault():
    return render_template('login.html')

@app.route('/ABOUT')
def ABOUT():
    return render_template('about.html')

@app.route('/SERVICES')
def SERVICES():
    return render_template('services.html')

@app.route('/dashboard.html')
def dashboard():                                        #connect to database to fetch user data
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True , port=5001)
       