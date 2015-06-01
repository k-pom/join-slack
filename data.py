from flask import flash
import requests
import os
import json

base_url = "https://api.orchestrate.io/v0/team/"
auth = (os.environ['orchestrate'], '')

def list_teams():
    teams = requests.get(base_url, auth=auth).json()
    return teams['results']

def get_team(team):
    return requests.get(base_url + team, auth=auth).json()

def add_team(team, api_key, description, organization):

    data = {
        "team": team,
        "url": "https://" + team + ".slack.com",
        "api_key": api_key,
        "description": description,
        "organization": organization
    }
    response = requests.put(base_url + team, json.dumps(data), headers={"Content-Type": "application/json"}, auth=auth)
    if response.status_code > 299:
        flash(response.json().get('message'))
        return False

    return True
