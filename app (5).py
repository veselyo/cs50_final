import sqlite3
from helpers import make_standings, convertinput, get_last_round, get_next_round, apology, login_required, get_fixture_ids, get_odds, get_fixtures_info, check_bet, get_status
import sys
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import pprint

# Define constant for the season year
season = 2022

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies) – Finance
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# From finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = rows.fetchall()
        print(rows)

        # Ensure username exists and password is correct
        if not len(rows) or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Close SQL connection
        conn.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        # Gets username, passsword, and confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must provide confirmation", 400)

        elif password != confirmation:
            return apology("password and confirmation do not match", 400)

        # Hashes password
        hash = generate_password_hash(password)

        # Check if username is taken
        check = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        check = check.fetchall()
        if len(check):
            conn.close
            return apology("username is taken", 400)

        # Insert user into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                       (username, generate_password_hash(request.form.get("password"))))
            conn.commit()

        # Log In user
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = user.fetchone()
        session["user_id"] = user
        # Close SQL connection
        conn.close()

        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/account")
@login_required
def account():
    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    bets = db.execute("SELECT * FROM bets WHERE user_id = ?", (13,))
    bets = bets.fetchall()
    if any(isinstance(el, list) for el in bets):
        return
    else:
        # Info that we will display
        info = get_fixtures_info(976458)
        if check_bet(976458):
            status = "Active"
        else:
            bet = db.execute("SELECT bet FROM bets WHERE user_id = ?", (13,))
            bet = bet.fetchone()
            result = get_status(976458)
            if result[bet[0]]["winner"]:
                status = "Bet Won"
            else:
                status = "Bet Lost"
        print(status)
        return render_template("account.html")


@app.route("/premierleague")
@login_required
def premierleague():
    input = "Premier League"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("premierleague.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/bundesliga")
@login_required
def bundesliga():
    input = "Bundesliga"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("bundesliga.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/la_liga")
@login_required
def la_liga():
    input = "La Liga"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("la_liga.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/ligue_one")
@login_required
def ligue_one():
    input = "Ligue 1"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("ligue_one.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/serie_a")
@login_required
def serie_a():
    input = "Serie A"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("serie_a.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/wcbetting", methods=["GET", "POST"])
@login_required
def worldcup():
    input = "World Cup"

    if request.method == "GET":

        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Gets the id of fixtures we are going to display
        fixtures = get_fixture_ids(convertinput(db, input), season)

        # Returns dictionary of odds, in format of home away for every fixture
        odds = get_odds(convertinput(db, input), season, fixtures)

        # Gets the information about fixtures
        info = get_fixtures_info(fixtures)

        length = len(info)

        conn.close()

        return render_template("wcbetting.html", odds = odds, info = info, length = length, fixtures = fixtures)

    else:

        fixture = request.form.get("fixture")
        team = request.form.get("team")
        odds = request.form.get("odds")
        money = request.form.get("money")

        # print(fixture, team, odds, money)

        if not fixture or not team or not odds:
            return apology("Click a Button to Bet!", 400)

        if not money:
            return apology("Put in Money", 400)

        if not money.isdigit():
            return apology("Invalid amount", 400)
        money = int(money)

        if money < 10:
            return apology("The minimum bet amount is 10$")

        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Update user balance
        print(session["user_id"])
        current = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
        current = current.fetchone()
        current = int(current[0])
        money = int(money)

        if current < money:
            return apology("Can't afford")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (current-money, session["user_id"]))


        # Update history
        db.execute("INSERT INTO bets (user_id, amount, fixture, bet) VALUES (?, ?, ?, ?)", ((session["user_id"]), money, fixture, team, ))

        return redirect("/")



@app.route("/wcstandings")
@login_required
def wcstandings():
    input = "World Cup"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    index = list(standings.keys())
    index = index[0]
    thead = standings[index][0]
    # Close SQL connection
    conn.close()

    return render_template("wcstandings.html", standings = standings, thead = thead)