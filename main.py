from flask import Flask, request, redirect, url_for, session
import boto3
import os
import hmac
import hashlib
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuração do Amazon Cognito
AWS_REGION = os.environ.get('AWS_REGION')
USER_POOL_ID = os.environ.get('USER_POOL_ID')
CLIENT_ID = os.environ.get('APP_CLIENT_ID')
APP_CLIENT_ID = os.environ.get('APP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

@app.route('/')
def home():
    if 'access_token' in session:
        return f'Hello, {session["username"]}! <a href="/logout">Logout</a>'
    else:
        return 'Bem-vindo! <a href="/login">Login</a>'

@app.route('/login')
def login():
    return redirect(f'https://aiflow-hyland-sso-teste.auth.us-east-1.amazoncognito.com/login?client_id=34gm1o6lojq9nelj5g4tcq6hfs&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fgoogle.com')

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return 'Erro durante o login.'

    access_token = request.args['access_token']
    id_token = request.args['id_token']

    session['access_token'] = access_token

    # Use o SDK da AWS (boto3) para obter informações do usuário
    client = boto3.client('cognito-idp', region_name=AWS_REGION)
    response = client.get_user(
        AccessToken=access_token
    )

    session['username'] = response['Username']

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
