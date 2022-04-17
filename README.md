# Async Django Kickstart

## GET google-contacts (people) using asyncio with Django 4.x

* Trying out async features of Django 4.x
* For fetching contacts used aiogoogle==3.2.1

## DIRECTORY STRUCTURE

* login - user management apps of **GOOGLE CONTACTS** app
* socialauth - Django project and settings of **GOOGLE CONTACTS** app

### SETTING UP DEVELOPMENT ENVIRONMENT API

```shell
python3 -m venv ./venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### MIGRATION

* To create migration file
  
  ```shell
  python manage.py makemigrations
  ```
  
* To migrate migration file
  
  ```shell
  python manage.py migrate
  ```

* To run application
  
  ```shell
  uvicorn socialauth.asgi:application --reload 
  ```

### SETUP google-auth

* goto: <https://console.cloud.google.com/apis/credentials/oauthclient>
* Enter Authorized JavaScript origins and Authorized redirect URIs
* Create OAuth client ID
* goto: <http://localhost:8000/admin/socialaccount/socialapp/add/>
* Fill with OAuth credentials and save
* Download OAuth JSON file.
* Example of JSON file:

```json
{
  "web": {
    "client_id": "{CLIENT_ID}",
    "project_id": "{PROJECT_ID}",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "{CLIENT_ID}",
    "redirect_uris": [
      "http://localhost:8000/accounts/google/login/callback/"
    ],
    "javascript_origins": [
      "http://localhost"
    ]
  }
}
```

* goto: <http://localhost:8000/contacts/list/> to see all your contacts

### APPLICATION DEPENDENCIES MODULE

* Django 4.x
* Python 3.x

#### STARTING SERVERS

* To run application server:
  
  ```shell
  uvicorn socialauth.asgi:application --reload 
  ```
