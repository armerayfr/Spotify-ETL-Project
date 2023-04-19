import requests
import secrets
import hashlib
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Set the client ID and secret obtained from the Spotify Developer Dashboard
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


# endpoint
# Set the authorization endpoint URL
auth_url = 'https://accounts.spotify.com/authorize'
# Set the token endpoint URL
token_url = 'https://accounts.spotify.com/api/token'
# Get the current playlist endpoint URL
curr_playlist_url = 'https://api.spotify.com/v1/me/player/recently-played'


def access_token():
    # Set the redirect URI for your application
    redirect_uri = 'https://example.com/callback'

    # Generate a random string for the state parameter
    state = secrets.token_urlsafe(16)

    # Generate a random string for the code verifier
    code_verifier = secrets.token_urlsafe(64)

    # Calculate the code challenge using SHA-256 and base64url encoding
    code_challenge_bytes = hashlib.sha256(code_verifier.encode('ascii')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_bytes).rstrip(b'=').decode('ascii')

    # Set the parameters for the authorization request
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
        'state': state,
        'scope': 'user-read-recently-played'
    }

    # Send the authorization request and redirect the user to the authorization page
    auth_response = requests.get(auth_url, params=auth_params)
    auth_url_with_params = auth_response.url
    print(f'Open this URL in your browser to authorize the application:\n{auth_url_with_params}')

    # Wait for the user to authorize the application and get redirected back to the redirect URI
    callback_url = input('Paste the callback URL from your browser here:\n')

    # Extract the authorization code and state parameter from the callback URL
    callback_params = dict(x.split('=') for x in callback_url.split('?')[1].split('&'))
    callback_code = callback_params['code']
    callback_state = callback_params['state']

    # Verify that the state parameter matches the one generated earlier
    if callback_state != state:
        raise Exception('State parameter mismatch')

    # Set the parameters for the token request
    token_params = {
        'grant_type': 'authorization_code',
        'code': callback_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Send the token request and get the access token and refresh token
    token_response = requests.post(token_url, data=token_params)
    token_data = token_response.json()
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']

    print(f'Access token: {access_token}')
    print(f'Refresh token: {refresh_token}')

    with open('refresh_token.txt', 'w') as f:
        f.write(refresh_token)

    return access_token


def refresh_token():
    with open('refresh_token.txt', 'r') as f:
        refresh_token = f.read()

    # Set the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Send the POST request
    response = requests.post(token_url, data=data)

    # Parse the response JSON data
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']

    with open('refresh_token.txt', 'w') as f:
        f.write(refresh_token)

    return access_token