from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from slack import update_team, get_invite
from data import list_teams, get_team

app = Flask(__name__)
app.debug = True
app.secret_key = "super_secret"

@app.route('/')
def index():
    return render_template('index.html', teams=list_teams())

@app.route('/invite', methods=['POST', 'GET'])
def invite():

    team = get_team(request.args.get('team') or request.form.get('team', ""))
    email = request.form.get('email', "")

    if request.method == 'POST':
        if(get_invite(team['team'], team['api_key'], email)):
            return redirect("/")

    return render_template('invite.html', team=team, email=email)

@app.route('/add', methods=['POST', 'GET'])
def add():

    team = request.form.get('team', "")
    api_key = request.form.get('api_key', "")
    description = request.form.get('description', "")
    organization = request.form.get('organization', "")

    if request.method == 'POST':
        if(update_team(team, api_key, description, organization)):
            return redirect("/")

    return render_template('add.html', team=team, api_key=api_key, description=description, organization=organization)

if __name__ == '__main__':
    app.run()
