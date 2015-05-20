import requests
from flask import flash
from data import add_team

def slack_url(team):
    return 'https://'+ team + '.slack.com/api'

def get_invite(team, api_key, email):
    url = slack_url(team) + '/users.admin.invite'
    response = requests.post(url, {
        "email": email,
        "token": api_key,
        "set_active": True
    }).json()

    print response

    if response['ok'] == False:
        if response['error'] == "invalid_email":
            flash("Looks like slack doesn't think your email is good. Want to double check it? ")
        elif response['error'] == 'sent_recently':
            flash("Looks like we've already sent and invite recently. ")
        else:
            flash("We weren't able to get your invite.")

        return False

    flash("Your invite should be arriving soon!")
    return True

def update_team(team, api_key, description, organization):

    url = slack_url(team) + '/auth.test'
    response = requests.post(url, {"token": api_key}).json()
    if response['ok'] == False:
        if response['error'] == "not_authed":
            flash("We were not able to authenticate with slack. Double check your team and api_key")
        else:
            flash("An unknown error occurred")
            flash(response['error'])
        return False

    return add_team(team, api_key, description, organization)
