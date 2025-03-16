from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Change this to a strong key

# Fake database for storing infractions
infractions = []

# API authentication key (only the Raspberry Pi should know this)
API_KEY = "raspberry_secret_key"

# Dummy login credentials
USERNAME = "admin"
PASSWORD = "password123"

# API Route for Raspberry Pi to send data
@app.route("/api/upload", methods=["POST"])
def upload_data():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403  # Reject request if key is wrong

    data = request.json
    infractions.append(data)
    return jsonify({"message": "Data received"}), 200

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Try again."

    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Login">
        </form>
    '''

# Dashboard (Protected)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", infractions=infractions)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
