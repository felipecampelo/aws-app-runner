import boto3
from botocore.exceptions import NoCredentialsError

# Configuração do pool de usuários
user_pool_id = 'seu-user-pool-id'
client_id = 'seu-client-id'

# Inicialize o cliente Cognito
cognito_client = boto3.client('cognito-idp')

# Autenticação
username = 'seu-username'
password = 'sua-senha'

try:
    response = cognito_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
        ClientId=client_id
    )

    # Você receberá os tokens de autenticação no 'AuthenticationResult' do response
    print("Tokens de autenticação:", response['AuthenticationResult'])

except NoCredentialsError:
    print("Credenciais AWS não configuradas")

except Exception as e:
    print("Erro de autenticação:", e)


print('Hello World!')
