from flask import Flask , render_template, request, redirect
import jsonreg
import platform
import psutil
import sys
app = Flask('app')
global known_ips
known_ips = []
PORT = jsonreg.get.data("appdata\settings\port.json")
def shutdown_server():
    sys.exit()
@app.route('/')
def home():
    return render_template("homepage.html")
@app.route('/login')
def login():
    if request.remote_addr in known_ips:
        return redirect("/admin",200)
    return render_template("login.html")
@app.route('/signin')
def signin():
    password = request.args.get('password', type = str)
    print(password)
    print(jsonreg.get.data("appdata/password.json"))
    if(jsonreg.get.data("appdata\password.json") == password):
        known_ips.append(request.remote_addr)
        return "True"
    else:
        return "False"    
@app.route('/forgot')
def forgot():
    return render_template("forgot.html")
@app.route('/admin')
def admin():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    return render_template("admin.html")
@app.route('/exit')
def exit():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    shutdown_server()
    return "True"
@app.route('/info')
def info():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    return "OS:"+str(platform.system())+"<br>"+"OS Version:"+str(platform.version())+"<br>"+"Architecture:"+str(platform.architecture())
@app.route('/logout')
def logout():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    known_ips.remove(request.remote_addr)
    return "True"
@app.route('/cpu_usage')
def cpu_usage():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    return str(psutil.cpu_percent())+"%"
@app.route('/ram_usage')
def ram_usage():
    if request.remote_addr not in known_ips:
        return redirect("/login",200)
    return str(psutil.virtual_memory()[2])+"%"
app.run(host = '0.0.0.0', port = PORT,debug=True)