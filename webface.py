
from flask import Flask, render_template, request, redirect, url_for, session, Markup, flash
import functools

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




@app.route("/admin", methods=["GET"])
def admin():
    if 'user' in session:
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))










@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login/", methods=["POST"])
def login_post():
    jmeno = request.form.get('jmeno','')
    heslo = request.form.get('heslo','')
    url=request.args.get("url", "") 
    if jmeno and heslo == "12345":
        flash("Jsi přihlášen!", "success")
        session["user"] = jmeno
        if url:
            return redirect(url)
        else:
            return redirect(url_for("index"))
    else:
        flash("Nesprávné přihlašovací údaje", "error")
    return redirect(url_for("login", url=url))

@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("byl jsi odhlášen", "success")
    return redirect(url_for("index"))




