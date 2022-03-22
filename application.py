import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///manage.db")

@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT username , community, expertise FROM users WHERE type='staff' AND community=:comm ORDER BY expertise", comm=session["comm"])

    staff_list = []
    for row in rows:

        staff_list.append({
            "name": row["username"],
            "comm": row["community"],
            "special": row["expertise"].capitalize()
        })

    return render_template("index.html", user=session["username"], staff=staff_list)

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        redirect('/')
    else:
        if session["type"] == "staff":
            rows = db.execute("SELECT DISTINCT request_id, resident_id, status, description, requirement, req_t, accept_t FROM calls JOIN users ON resident_id WHERE users.community = :com AND calls.status = 'in progress' AND calls.staff_id = :uid", com = session["comm"], uid = session["user_id"])

            req_list = []
            for row in rows:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["resident_id"])
                req_list.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"],
                    "accepted": row["accept_t"]
                })

            rows2 = db.execute("SELECT DISTINCT request_id, resident_id, status, description, requirement, req_t, complete_t, s_description FROM calls JOIN users ON resident_id WHERE users.community = :com AND calls.status = 'completed' OR calls.status = 'closed' AND calls.staff_id = :uid", com = session["comm"], uid = session["user_id"])

            req_list2 = []
            for row in rows2:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["resident_id"])
                req_list2.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"],
                    "completed": row["complete_t"],
                    "s_desc": row["s_description"]
                })

            rows3 = db.execute("SELECT DISTINCT request_id, resident_id, status, description, requirement, req_t, complete_t, s_description, rating, complaints FROM calls JOIN users ON resident_id WHERE users.community = :com AND calls.status = 'closed' AND calls.staff_id = :uid", com = session["comm"], uid = session["user_id"])

            req_list3 = []
            for row in rows3:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=session["user_id"])
                req_list3.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"],
                    "completed": row["complete_t"],
                    "s_desc": row["s_description"],
                    "rating": row["rating"],
                    "r_desc": row["complaints"]
                })

            request_id = request.args.get('rid')
            completion_time = request.args.get('comp')
            description = request.args.get('desc')
            if request_id and completion_time and description:
                flash('Request Completed')
                db.execute("UPDATE calls SET status = 'completed', staff_id = :uid, complete_t = :ct, s_description = :sdc WHERE request_id = :rid", uid=session["user_id"], rid = request_id, ct = completion_time, sdc = description)

            return render_template('tasks.html', comp=req_list2, prog=req_list, clos=req_list3, comm=session["comm"])
        else:
            return apology("Forbidden", 403)

@app.route("/my_req", methods=["GET", "POST"])
@login_required
def my_req():
    if request.method == "POST":
        redirect('/')
    else:
        if session["type"] == "resident":
            rows = db.execute("SELECT DISTINCT request_id, resident_id, staff_id, status, description, requirement, req_t, accept_t FROM calls JOIN users ON resident_id WHERE users.community = :com AND ( calls.status = 'in progress' OR calls.status = 'pending' ) AND calls.resident_id = :uid", com = session["comm"], uid = session["user_id"])
            print(rows)

            req_list = []
            for row in rows:
                if row["staff_id"]:
                    name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["staff_id"])
                    req_list.append({
                        "id": row["request_id"],
                        "name": name[0]["username"],
                        "status": row["status"],
                        "description": row["description"],
                        "requirement": row["requirement"],
                        "time": row["req_t"],
                        "accepted": row["accept_t"]
                    })
                else:
                    name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["staff_id"])
                    req_list.append({
                        "id": row["request_id"],
                        "name": "None",
                        "status": row["status"],
                        "description": row["description"],
                        "requirement": row["requirement"],
                        "time": row["req_t"],
                        "accepted": row["accept_t"]
                    })

            rows2 = db.execute("SELECT DISTINCT request_id, staff_id, status, description, requirement, req_t, complete_t, s_description FROM calls JOIN users ON staff_id WHERE users.community = :com AND calls.status = 'completed' AND calls.resident_id = :uid", com = session["comm"], uid = session["user_id"])

            req_list2 = []
            for row in rows2:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["staff_id"])
                req_list2.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"],
                    "completed": row["complete_t"],
                    "s_desc": row["s_description"]
                })

            rows3 = db.execute("SELECT DISTINCT request_id, staff_id, status, description, requirement, req_t, complete_t, s_description, rating, complaints FROM calls JOIN users ON staff_id WHERE users.community = :com AND calls.status = 'closed' AND calls.resident_id = :uid", com = session["comm"], uid = session["user_id"])

            req_list3 = []
            for row in rows3:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["staff_id"])
                req_list3.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"],
                    "completed": row["complete_t"],
                    "s_desc": row["s_description"],
                    "rating": row["rating"],
                    "r_desc": row["complaints"]
                })

            request_id = request.args.get('rid')
            rating = request.args.get('rate')
            description = request.args.get('r_desc')
            print(request_id, rating)

            if request_id and rating:
                if int(rating) <= 3:
                    print("YESSS")
                    flash('Request Re-Opened')
                    db.execute("UPDATE calls SET status = 'in progress', rating = :rate, complaints = :desc WHERE request_id = :rid", rate = int(rating), desc = description, rid = request_id)
                else:
                    flash('Request Closed')
                    db.execute("UPDATE calls SET status = 'closed', rating = :rate WHERE request_id = :rid", rate = rating, rid = request_id)

            return render_template('my_req.html', comp=req_list2, prog=req_list, clos=req_list3, comm=session["comm"])
        else:
            return apology("Forbidden", 403)

@app.route("/schedule")
@login_required
def schedule():
    if session["type"] == 'staff':
        rows = db.execute("SELECT start_time, end_time, start_day, end_day FROM staffschedule WHERE user_id = :user", user=session["user_id"])

        if rows:
            return render_template('schedule.html', row=rows[0])
        else:
            return render_template('schedule.html', row=None)
    else:
        return apology("Forbidden", 403)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = :user", user=request.form.get("name"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["comm"] = rows[0]["community"]
        session["type"] = rows[0]["type"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/call", methods=["GET", "POST"])
@login_required
def call():
    if request.method == "POST":
        date = request.form.get("week")
        desc = request.form.get("description")
        reqr = request.form.get("req")
        status = "pending"

        if not date or not desc or not reqr:
            return apology('Please provide information to all fields')
        elif session["type"] == 'staff':
            return apology("Forbidden", 403)
        else:
            db.execute("INSERT INTO calls (resident_id, status, description, requirement, req_t) VALUES(:res, :sta, :des, :req, :rti)", res=session["user_id"], sta=status, des=desc, req=reqr, rti=date)
            flash('Request made!')
            return redirect('/')
    else:
        return render_template('call.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure if the confirmed password matches or not
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation must match password")

        elif not request.form.get("type"):
            return apology("must provide type of account")

        elif not request.form.get("community"):
            return apology("must provide community")

        elif request.form.get("type") == "staff":
            if not request.form.get("stype"):
                return apology("must provide staff speciality")

        rows = db.execute("SELECT * FROM users WHERE username = :user", user=request.form.get("name"))
        if len(rows) != 0:
            return apology("username already exists")

        registration = db.execute("INSERT INTO users (username, password, type, community, expertise) VALUES(:user, :passw, :t, :comm, :spe)",
                                  user=request.form.get("name"), passw=generate_password_hash(request.form.get("password")), t=request.form.get("type"), comm=request.form.get("community"), spe=request.form.get("stype"))

        if registration == None:
            return apology("registration error")

        # Success scenario
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/listr", methods=["GET", "POST"])
@login_required
def listr():
    if request.method == "POST":
        return redirect('/tasks')
    else:
        if session["type"] == "staff":
            rows = db.execute("SELECT DISTINCT request_id, resident_id, status, description, requirement, req_t FROM calls JOIN users ON resident_id WHERE users.community = :com AND calls.status != 'completed' AND calls.status != 'closed'", com = session["comm"])

            req_list = []
            for row in rows:
                name = db.execute("SELECT username FROM users WHERE id = :uid", uid=row["resident_id"])
                req_list.append({
                    "id": row["request_id"],
                    "name": name[0]["username"],
                    "status": row["status"],
                    "description": row["description"],
                    "requirement": row["requirement"],
                    "time": row["req_t"]
                })

            request_id = request.args.get('rid')
            accept_time = request.args.get('acct')
            if request_id:
                flash('Request Accepted')
                db.execute("UPDATE calls SET status = 'in progress', staff_id = :uid, accept_t = :at WHERE request_id = :rid", uid=session["user_id"], rid=request_id, at = accept_time)

            return render_template("listr.html", requirements=req_list, comm=session["comm"])
        else:
            return apology("Forbidden", 403)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
