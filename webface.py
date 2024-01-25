
from flask import Flask, render_template, request, redirect, url_for, session, Markup, flash
import functools
from sqlitewrap import SQLite
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")



@app.route("/kari", methods=["GET"])
def kari():
    return render_template("kari.html")




@app.route("/hamburger", methods=["GET"])
def hamburger():
    return render_template("hamburger.html")




@app.route("/lazane", methods=["GET"])
def lazane():
    return render_template("lazane.html")




@app.route("/vzkazy", methods=["GET"])
def admin():
    if 'user' not in session:
        return redirect(url_for("index"))
    with SQLite("db.sqlite") as cursor:
        response = cursor.execute("SELECT user, body, datetime, message.id FROM user JOIN message ON user.id = message.user_id ORDER BY datetime")
        response = response.fetchall() 
       
    return render_template("admin.html", response=response, d=datetime.datetime)
    

@app.route("/vzkazy", methods=["POST"])
def admin_post():
    with SQLite("db.sqlite") as cursor:
        response = cursor.execute("SELECT id FROM user WHERE user=?",[session["user"]])
        response = response.fetchone()
        user_id = list(response)[0]
    vzkaz = request.form.get('vzkaz')
    if vzkaz:
        with SQLite("db.sqlite") as cursor:
            cursor.execute('INSERT INTO message(user_id,body, datetime) VALUES(?,?,?)', [user_id, vzkaz, datetime.datetime.now()])
    
    return redirect(url_for("admin"))







@app.route("/register/", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/register/", methods=["POST"])
def register_post():
    jmeno = request.form.get("jmeno","")
    heslo1 = request.form.get("heslo1","")
    heslo2 = request.form.get("heslo2","")
    if len(heslo1) < 5:
        flash("Heslo musí mít aspoň 5 znaků", "error")
        return redirect(url_for("register"))
    if len(jmeno) < 5:
        flash("Jmeno musí mít aspoň 5 znaků", "error")
        return redirect(url_for("register"))
    if heslo1 != heslo2:
        flash("musíte zadat stejné heslo", "error")
        return redirect(url_for("register"))
    
    hash_ = generate_password_hash(heslo1)
    try:
        with SQLite("db.sqlite") as cursor:
            cursor.execute('INSERT INTO user(user,password) VALUES(?,?)', [jmeno, hash_])
            flash(f"uživatel {jmeno} byl přidán", "success")
    except:
        flash("Uživatle už jednou existuje", "error")
    return redirect(url_for("register"))









@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login/", methods=["POST"])
def login_post():
    jmeno = request.form.get('jmeno','')
    heslo = request.form.get('heslo','')
    url=request.args.get("url", "") 
    with SQLite("db.sqlite") as cursor:
        response = cursor.execute("SELECT user, password FROM user WHERE user = ?", [jmeno]) 
        response = response.fetchone()
        if response:
            user, password = response
            if check_password_hash(password, heslo):
                flash("Jsi přihlášen!", "success")
                session["user"] = jmeno
                if url:
                    return redirect(url) 
                else:
                    return redirect(url_for("index"))
        flash("Nesprávné přihlašovací údaje", "error")
        return redirect(url_for("login", url=url))

@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("byl jsi odhlášen", "success")
    return redirect(url_for("index"))




