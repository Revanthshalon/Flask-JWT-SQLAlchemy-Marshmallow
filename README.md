# Flask-JWT-SQLAlchemy-Marshmallow

Flask Project with Authentication and Data base Connectivity with Token Blacklisting

## How to set this app to run in Heroku
- Clone this repo
- Link the repo to heroku
- Add Heroku Postgres Free Database
- Set config vars as 
  - key:FLASK_APP value:app
  - key:FLASK_ENV value:production
- Go to more -> Run console.
- run command 'flask db upgrade'
- Start Calling the API's as it is .


# API End Points
- host:/token/register
- host:/token/login
- host:/token/refresh
- host:/token/logout
- host:/token/logout2
