This a personal learning track i'm using to learn and improve on my knowledge of building APIs with DRF

Steps to run the django project contained in this repo

 1. clone repo (or download manually) and navigate to folder directory on any CLI
 2. on the CLI, run  `pip install -r requirements.txt` to install project dependencies into current working environment
 3. you may use any database of your choice(i used postgres)
 4. adjust the *DATABASE* settings located in the [core/settings.py](https://github.com/themaleem/simpu-code-challenge/blob/master/core/settings.py) file to fit the your database of your choice.
 5. on the CLI, run migrations , with command `python manage.py makemigrations`  followed by `python manage.py migrate`
 6. run  `python manage.py loaddata data.json` to load the *data.json* into the database
 7. run `python manage.py runserver`
 8. study config/urls.py for url nagivations