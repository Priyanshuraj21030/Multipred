from flask import Flask, render_template, request, redirect, url_for, flash, session
import boto3
from warrant import Cognito
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# AWS Cognito Configuration
AWS_REGION = 'your-region'  # e.g., 'us-east-1'
COGNITO_USER_POOL_ID = 'your-user-pool-id'
COGNITO_APP_CLIENT_ID = 'your-app-client-id'
COGNITO_APP_CLIENT_SECRET = 'your-app-client-secret'

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

@app.route('/auth/google')
def google_auth():
    # Redirect to Cognito hosted UI for Google sign-in
    cognito_domain = f'https://your-domain.auth.{AWS_REGION}.amazoncognito.com'
    redirect_uri = 'http://localhost:5000/auth/callback'
    
    auth_url = (
        f'{cognito_domain}/oauth2/authorize?'
        f'client_id={COGNITO_APP_CLIENT_ID}&'
        f'response_type=code&'
        f'scope=email+openid+profile&'
        f'redirect_uri={redirect_uri}&'
        f'identity_provider=Google'
    )
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    try:
        code = request.args.get('code')
        cognito_domain = f'https://your-domain.auth.{AWS_REGION}.amazoncognito.com'
        token_endpoint = f'{cognito_domain}/oauth2/token'
        redirect_uri = 'http://localhost:5000/auth/callback'
        
        # Exchange authorization code for tokens
        response = requests.post(
            token_endpoint,
            auth=(COGNITO_APP_CLIENT_ID, COGNITO_APP_CLIENT_SECRET),
            data={
                'grant_type': 'authorization_code',
                'client_id': COGNITO_APP_CLIENT_ID,
                'code': code,
                'redirect_uri': redirect_uri
            }
        )
        
        tokens = response.json()
        
        # Get user info from ID token
        id_token = tokens['id_token']
        user_info = jwt.decode(id_token, verify=False)
        
        # Store user info in session
        session['user_id'] = user_info['sub']
        session['user_email'] = user_info['email']
        session['user_name'] = user_info.get('name', '')
        
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        print(f"Error in auth callback: {str(e)}")
        flash('Authentication failed')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Initialize Cognito user
            user = Cognito(
                user_pool_id=COGNITO_USER_POOL_ID,
                client_id=COGNITO_APP_CLIENT_ID,
                username=email
            )
            
            # Authenticate user
            user.authenticate(password=password)
            
            # Store tokens in session
            session['access_token'] = user.access_token
            session['id_token'] = user.id_token
            session['refresh_token'] = user.refresh_token
            
            # Store user info
            session['user_email'] = email
            session['user_name'] = user.get_user().get('name', '')
            
            flash('Login successful!')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash('Invalid email or password')
            print(f"Login error: {str(e)}")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = f"{request.form['firstName']} {request.form['lastName']}"
        
        try:
            # Create user in Cognito
            response = cognito_client.sign_up(
                ClientId=COGNITO_APP_CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name}
                ]
            )
            
            flash('Account created successfully! Please check your email for verification.')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Error creating account')
            print(f"Signup error: {str(e)}")
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 