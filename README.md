# A  a book review website
- A website that let user register and log in and allows user search and write reviews for a particular book and see the reviews made by others.
- Arteeas generate a music of gallery list based on you prference.

- Utilized Python Framework Flask to set up server, and used a third-party API by Goodreads, another book review website, to allow users browse a broader set of reviews.

## To set up virtual environment
- make a virtual enviroment

        virtualenv bookees_env

- activate the virtual enviroment

        source bookees_env/bin/activate

- to exit the current virtual enviroment

        deactivate

 - to intall all packages used in this project

        pip install -r requirements.txt

  - to delete the virtual enviroment  <br>

        rm -rf bookees_env     

## To create database in terminal using SQLite
- import modesl from arteeas package

       from arteeas.models import User, Music

- create locak db file

       db.create_all()

- to make query

       User.query.all()

# Deploy on Heroku
- check database url and make sure it is set to the the psql url on heroku

        heroku config
- create an file **Procfile** @ your repo directory arteeas with the line below:

        web: gunicorn arteeas.wsgi

- create wsgi.py @ your repo sub-directory arteeas
- more info at https://devcenter.heroku.com/articles/python-gunicorn
