from datetime import datetime
from unittest.mock import MagicMock
import boto3
from botocore.exceptions import ClientError
from botocore.stub import ANY
import pytest
import os

from cognito_idp_actions import CognitoIdentityProviderWrapper

cognito_idp_client = boto3.client('cognito-idp', region_name='us-east-1')

user_pool_id = os.environ.get('USER_POOL_ID')
client_id = os.environ.get('APP_CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
cognito_password = os.environ.get('COGNITO_PASSWORD')

# Crie uma instância do CognitoIdentityProviderWrapper
cognito_wrapper = CognitoIdentityProviderWrapper(cognito_idp_client, user_pool_id, client_id, client_secret)

try:
    # Chame a função start_sign_in para iniciar o processo de login
    result = cognito_wrapper.start_sign_in('teste', cognito_password)
    print(result)

    # Verifique o resultado para determinar como proceder
    if 'AuthenticationResult' in result:
        # O login foi bem-sucedido e você pode obter um token de acesso
        access_token = result['AuthenticationResult']['AccessToken']
        print(f'Login bem-sucedido! Token de acesso: {access_token}')
except:
    pass
