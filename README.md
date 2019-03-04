# CollabPRO
An application for creating future teams and projects.


## Installation Guide
- Ensure you have Python 3, virtualenv and postgresQL installed
- Clone the repository `git clone https://github.com/johnchuks/CollabPRO-API.git`
- Create your virtual environment `virtualenv -p python3 <name of env>`
- Activate the environment `source <name of env>/bin/activate`
- Change your directory `cd CollabPRO-API`
- Install all dependencies `pip install -r requirements.txt`
- create a .env file using the `.env-sample`
- Ensure the secret key to the django app is added to the `.env` file (you can use a secret key of your choice).
- Run tests like so `python manage.py test`.
- Start the app with `python manage.py runserver`.
