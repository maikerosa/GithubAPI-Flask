from flask import Flask
from flask import render_template, url_for, request, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

oauth = OAuth(app)
app.config['SECRET_KEY'] = 'secret'
app.config['GITHUB_CLIENT_ID'] = "04707c9965ca9d02c972"
app.config['GITHUB_CLIENT_SECRET'] = "4c60957004c8e8de390377b27b6df6e50ef0d703"

github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)

app_url_github_login = "/login/github"

@app.route("/")
def index():
    return render_template("index.html", github_login=app_url_github_login)

@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    return render_template("snippets.html", user=resp)

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)