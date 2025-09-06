from flask import Flask, request, session, redirect, url_for, render_template, jsonify,send_from_directory
import os, hashlib
from flask.templating import render_template

from db import init_db, register_user, verify_user, add_block, get_chain_db

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this!

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER   
# Initialize DB at startup
init_db()



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            register_user(username, password)
            return redirect(url_for("login"))
        except Exception as e:
            return f"Registration failed: {str(e)}"

    # return render_template_string(REGISTER_HTML)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("upload_file"))
        else:
            return "Invalid credentials"
    # return render_template_string(LOGIN_HTML)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))



@app.route("/", methods=["GET", "POST"])
def upload_file():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    app.config["UPLOAD_FOLDER"] = os.path.join(UPLOAD_FOLDER, username)
    if request.method == "POST":
        f = request.files["file"]
        if f.filename == "":
            return "No file selected"

        user_folder = os.path.join(UPLOAD_FOLDER, username)
        os.makedirs(user_folder, exist_ok=True)
        
        filepath = os.path.join(user_folder, f.filename)
        f.save(filepath)

        # Hash file
        file_hash = hashlib.sha256(open(filepath, "rb").read()).hexdigest()

        # Get last block for prev_hash
        chain = get_chain_db(username)
        prev_hash = chain[-1]["filehash"] if chain else "0"

        # Add block
        add_block(username, f.filename, file_hash, prev_hash)

        return f"File uploaded and added to blockchain: {f.filename}"

    return render_template("upload.html" , username=username)


@app.route("/myfiles")
def myfiles():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    chain = get_chain_db(username)
    return jsonify(chain)

@app.route("/download")
def downloads():
    # List all files in the uploads directory

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("download.html", files=files)

# Route: Serve a specific file
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
