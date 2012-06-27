#never ever use this code in your production 
#This is meant to very simplistic example just to show the flow
#Encrypt before saving password and seed in DB 

from bottle import get, post, request
from bottle import route, run
from bottle import redirect
from bottle import response
import pyg2fa

@get('/') 
def login_form():
    return '''<form method="POST" action="/login">
                name:<input name="name"     type="text" />
                password:<input name="password" type="password" />    
                <input type="submit" />         
              </form>'''

@post('/login') 
def login_submit():
    name     = request.forms.get('name')
    password = request.forms.get('password')
    if check_login(name, password):
    	response.set_cookie("g2fa_account", name, secret='somesecretkey')
    	redirect("/otp")
    else:
        return "<p>Login failed</p>"

@get('/otp') 
def otp_form():
	name = request.get_cookie("g2fa_account", secret='somesecretkey')
	if name:
		return '''<form method="POST" action="/otp">
		otp:<input name="otp" type="otp" />
		<input type="submit" />               
		</form>'''
	else:
		redirect("/")
              
@get('/logout') 
def logout():
	name = request.get_cookie(("g2fa_account"), secret='somesecretkey')
	response.delete_cookie("g2fa_account")
	redirect("/")

@post('/otp') 
def otp_form():
   otp     = request.forms.get('otp')
   name = request.get_cookie("g2fa_account", secret='somesecretkey')
   if check_otp(name, otp):
		return "Hello %s. Welcome back. <a href='/logout'>logout</a>" % name
   else:
		return "<p>Login Failed</p>"

def check_login(name, password):
	for a in dummyDB():
		if a['user']==name and a['password'] == password:
			return True
		else:
			return False

def check_otp(name, otp):
	for a in dummyDB():
		if a['user']==name:
			USER_SECRET_INITIAL_OTP_SEED =a['otp_seed']
	if pyg2fa.validate(USER_SECRET_INITIAL_OTP_SEED, int(otp), 4):
		return True
	else:
		return False


def dummyDB():
	return [{"user":"thej","password":"notsafe", "otp_seed":"KKK67SDNLXIOG65U"},{"user":"ram","password":"yeahokay", "otp_seed":""}]

print """To test please access the following url and \n
	scan the QR code into your Google Authenicator App.\n 
	Now your 2f setup for as user thej is complete. \n
	Use this for OTP while loginng in as thej.\n
	This URL is only for the eyes of user thej.\n
	This uses otp_seed which is generated when use was created and is unique to user.\n
	URL = """+ pyg2fa.qrCodeURL("http://g2fa-example.com", "KKK67SDNLXIOG65U")+"\n\n\n"

run(host='localhost', port=8080, debug=True)