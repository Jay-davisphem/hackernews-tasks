# EXPRESS NEWS PROJECT by David Oluwafemi 

This repository contains a web services(both web application and API), of a news crawling website(Done as a Fullstack Developer task given by [Dowstrademus](https://www.drattraderapp.com/).
I made use of Python(Django, Django rest framework), HTML and CSS. I used DRF because it's faster and better than writing all the reusable code myself and whereas, it is a good Software Development practice. 

To run this project on your local machine, please follow the following steps:

* Clone this repository ```git clone https://github.com/Jay-davisphem/hackernews-tasks.git```
* cd into hackernews-tasks or whatever you renamed your folder into
* create a new virtualenv by doing ```python3 -m venv <your venv name>```(this works for linux)
* activate it using ```. .<your venv name>/bin/activate```
* install the requirements py running ```pip install -r requirements.txt```
* You can use sqlite3 as your local Database or PostgreSQL
  * To use sqlite3 do nothing and continue to the next step
  * Or To use PostgreSQL just create a .env file and define ```USE_PROD=1```, ```DB_NAME=<your database name>```` and ``DB_PWD-<your created postgresql database password```
* Run migrations by doing ```python -m manage.py makemigrations``` and ```python -m manage.py migrate```
* This projects use celery to do background tasks, so spin up celery worker and beat using the following commands still inside virtualenv:
  * ```python -m celery -A newsapp worker -l info```
  * ```python -m celery -A newsapp beat -l info```
* Run the server using ```python -m manage.py runserver```
Links to the API Documentations is part of the webapp navbar items and you can find them in ```/api/swagger or /api or /api/redoc```. They're  automatically generated and well documented


## FEW OF THE ACCOMPLISHMENTS AND THE REQUIRED

  - [x] Use Django. Make a new virtualenv and pip install it;
  - [x] Make a scheduled job to sync the published news to a DB every 5 minutes. You can start with the latest 100 items, and sync every new item from there. Note: there are several types of news (items), with relations between them;
  - [x] Implement a view to list the latest news;
  - [x] Allow filtering by the type of item;
  - [x] Implement a search box for filtering by text;
  - [x] As there are hundreds of news you probably want to use pagination or lazy loading when you display them.

It is also important to expose an API so that our data can be consumed:

  - [x] GET  : List the items, allowing filters to be specified;
  - [x] POST  : Add new items to the database (not present in Hacker News);

- [x] Bonus

  - [x] Only display top-level items in the list, and display their children (comments, for example) on a detail page;
  - [x] In the API, allow updating and deleting items if they were created in the API (but never data that was retrieved from Hacker News);
  - [x] Be creative! :)

