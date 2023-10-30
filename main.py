from flask import Flask, request, redirect, url_for, session
import boto3
import os

app = Flask(__name)
app.secret_key = os.urandom(24)

# Configuração do Amazon Cognito
AWS_REGION = os.environ.get('AWS_REGION')
USER_POOL_ID = os.environ.get('USER_POOL_ID')
APP_CLIENT_ID = os.environ.get('APP_CLIENT_ID')
IDENTITY_POOL_ID = os.environ.get('IDENTITY_POOL_ID')
# AWS_REGION = 'sua-regiao'
# USER_POOL_ID = 'seu-user-pool-id'
# APP_CLIENT_ID = 'seu-client-id'
# IDENTITY_POOL_ID = 'seu-identity-pool-id'

@app.route('/')
def home():
    if 'access_token' in session:
        return f'Hello, {session["username"]}! <a href="/logout">Logout</a>'
    else:
        return 'Bem-vindo! <a href="/login">Login</a>'

@app.route('/login')
def login():
    return redirect(f'https://{AWS_REGION}.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id={APP_CLIENT_ID}&redirect_uri={url_for("callback", _external=True)}')

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
