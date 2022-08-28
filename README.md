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
  * Or To use PostgreSQL just create a database with psql or any services you use like pgAdmin and create .pg_service.conf file in your system home directory if you are on linux(You will have to set the directory to find the file if you are on windows using ```setx PGSYSCONFDIR "<path_to_dir>"``` and then define pg_service.conf in that specified directory)(please follow https://docs.djangoproject.com/en/4.0/ref/databases/#postgresql-notes for the content of .pg_service.conf(pg_service.conf for windows) then define ```USE_PROD=1``` in the .env file and ```localhost:5432:<DATABASE NAME>:<USER>:<PASSWORD>``` in a .my_pgpass located in your root project folder where .env is located.
  - [ ] *NOTE:* I use this resources to set the database up. [4.0 POSTGRES SETUP](https://docs.djangoproject.com/en/4.0/ref/databases/#postgresql-notes) and this image
  ![POSTGRES SETTING IMAGE](/static/img/database_guide.png)

* Run migrations by doing ```python -m manage.py makemigrations``` and ```python -m manage.py migrate```
* This projects use Advanced Python Scheduler for job scheduling of news fetching from hackernews so no setup needed
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
  
  
## CHALLENGES, DECISIONS AND PLANS(It'll continue to be upadated)
* I intended to use celery for job scheduling initially but decide otherwise when I realised it's no more supported and maintained from version 4.x for windows [celery support for windows](https://docs.celeryq.dev/en/stable/faq.html#windows). I then researched on other options like [huey](https://huey.readthedocs.io/en/latest/) among others before I decided to us [Python advanced schduler](https://apscheduler.readthedocs.io/en/3.x/). Which works well accross all platform. It's OS dependent just like python.
* When my tasks was running twice, I researched and realized that starting my tasks from AppConfig.ready method is the problems. It'll always run twice unless I put --noreload when running my server. But I solved it by starting the tasks in the base urls.py
* Hackernews api use proxy to store all there models i.e all the models(story, poll, comment, pollopt and job use just one table. I based my new news fetch on the fact that the latest item will have the highest id. So after the initial 100 news items has been fetched, for subsequent fetch I check if the highest id has already been saved in the database, I won't make a recurring fetch, but once it's not there the latest news is fetched every 5 minutes.
* This branch is my task submission, but you can check [this](https://github.com/Jay-davisphem/hackernews-tasks/tree/main) branch which contains my celery version code. This branch(submitted) is already deployed on heroku while the celery version is having problems on heroku but is working perfectly locally.
Note I intensionally made this branch the default.
* I plan to dockerize this app so that I won't need to care about what OS it's been run on locally.
