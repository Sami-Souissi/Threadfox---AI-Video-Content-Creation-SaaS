import webbrowser
from pathlib import Path
from flask import Flask, send_file


# Used "tomlkit" instead of "toml" because it doesn't change formatting on "dump"
import tomlkit
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

import utils.gui_utils as gui

# Set the hostname
HOST = "localhost"
# Set the port number
PORT = 4000

# Configure application
app = Flask(__name__, template_folder="GUI")

# Configure secret key only to use 'flash'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Display index.html
@app.route("/")
def index():
    return render_template("index.html", file="videos.json")


@app.route("/backgrounds", methods=["GET"])
def backgrounds():
    return render_template("backgrounds.html", file="backgrounds.json")
#Display to do
@app.route('/new')
def new_page():
    return render_template('new.html')
@app.route('/new2')
def new_page2():
    return render_template('new2.html')



@app.route("/background/add", methods=["POST"])
def background_add():
    # Get form values
    youtube_uri = request.form.get("youtube_uri").strip()
    filename = request.form.get("filename").strip()
    citation = request.form.get("citation").strip()
    position = request.form.get("position").strip()

    gui.add_background(youtube_uri, filename, citation, position)

    return redirect(url_for("backgrounds"))


@app.route("/background/delete", methods=["POST"])
def background_delete():
    key = request.form.get("background-key")
    gui.delete_background(key)

    return redirect(url_for("backgrounds"))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    config_load = tomlkit.loads(Path("config.toml").read_text())
    config = gui.get_config(config_load)

    # Get checks for all values
    checks = gui.get_checks()

    if request.method == "POST":
        # Get data from form as dict
        data = request.form.to_dict()

        # Change settings
        config = gui.modify_settings(data, config_load, checks)

    return render_template(
        "settings.html", file="config.toml", data=config, checks=checks
    )


# Make videos.json accessible
@app.route("/videos.json")
def videos_json():
    return send_from_directory("video_creation/data", "videos.json")

@app.route('/image')
def serve_image():
    return send_file('assets/backgrounds/LOGO.png', mimetype='image/png')
@app.route('/favicon.ico')
def serve_favicon():
    return send_file('assets/backgrounds/favicon.ico', mimetype='image/x-icon')


@app.route('/image_i')
def serve_inverted_image():
    return send_file('assets/backgrounds/LOGO_i.png', mimetype='image/png')

# Make backgrounds.json accessible
@app.route("/backgrounds.json")
def backgrounds_json():
    return send_from_directory("utils", "backgrounds.json")


# Make videos in results folder accessible
@app.route("/results/<path:name>")
def results(name):
    return send_from_directory("results", name, as_attachment=True)


# Make voices samples in voices folder accessible
@app.route("/voices/<path:name>")
def voices(name):
    return send_from_directory("GUI/voices", name, as_attachment=True)
#test 
import subprocess
import os


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    print("Button clicked!") # Add this line to check if the function is being called
    os.system('python main.py') 
    cmd = 'python main.py'

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print('Command executed successfully')
        
    else:
        print('Error executing command:', error)
    return render_template('index.html')
    

# Run browser and start the app
if __name__ == "__main__":
    webbrowser.open(f"http://{HOST}:{PORT}", new=2)
    print("Website opened in new tab. Refresh if it didn't load.")
    app.run(port=PORT)


