from flask import Flask, render_template, redirect, url_for, request

from forms import TeamForm, ProjectForm
from model import db, User, Team, Project, connect_to_db

app = Flask(__name__)

app.secret_key = "keep this secret"

user_id = 1

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", title = "Project Tracking App", page = "home", team_form = team_form, project_form = project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Project(project_name, completed, team_id, description = description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/teams")
def teams():
    user = User.query.get(user_id)
    return render_template("teams.html", title = "Teams", page = "teams", teams = user.teams)

@app.route("/projects")
def projects():
    user = User.query.get(user_id)
    projects = user.get_all_projects()
    return render_template("projects.html", title = "Projects", page = "projects", projects = projects)

@app.route("/update-team/<team_id>", methods=["GET", "POST"])
def update_team(team_id):
    form = TeamForm()
    team = Team.query.get(team_id)
    if request.method == "POST":
        if form.validate_on_submit():
            team.team_name = form.team_name.data
            db.session.add(team)
            db.session.commit()
            return redirect(url_for("teams"))
        else:
            return redirect(url_for("home"))

    else:
        return render_template("update-team.html", title = f"Update {team.team_name}", page = "teams", team = team, form = form)

@app.route("/update-project/<project_id>", methods=["GET", "POST"])
def update_project(project_id):
    form = ProjectForm()
    form.update_teams(User.query.get(user_id).teams)
    project = Project.query.get(project_id)

    if request.method == "POST":
        if form.validate_on_submit():
            project.project_name = form.project_name.data
            if len(form.description.data) > 0:
                project.description = form.description.data
            project.completed = form.completed.data
            project.team_id = form.team_selection.data
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("projects"))
        else:
            return redirect(url_for("home"))   
    else:
        return render_template("update-project.html", title = f"Update {project.project_name}", page = "projects", project = project, form = form)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)