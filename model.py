import os
from flask_sqlalchemy import SQLAlchemy


# to run this, go to Gitbash and type 'soruce config.sh' then run model.py

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

    teams = db.relationship("Team", backref = "user", lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_all_projects(self):
        projects = []

        for team in self.teams:
            for project in team.projects:
                projects.append(project)

        return projects

class Team(db.Model):

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    projects = db.relationship("Project", backref = "team", lazy = True)

    def __init__(self, team_name, user_id):
        self.team_name = team_name
        self.user_id = user_id

class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)

    def __init__(self, project_name, completed, team_id, **kwargs):
        self.project_name = project_name
        self.completed = completed
        self.team_id = team_id

        if "description" in kwargs:
            self.description = kwargs["description"]


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")