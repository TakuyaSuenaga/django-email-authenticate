# django-email-authenticate
Basic Django project with the fewest codes that authenticate with an email address instead of a username.

```sh
$ python3 --version
Python 3.9.1
```

## How to Run

```shell
$ python3 -m pip install -r requirements.txt
...
Installing collected packages: typing-extensions, sqlparse, asgiref, fontawesomefree, Django
Successfully installed Django-4.0.6 asgiref-3.7.2 fontawesomefree-6.1.2 sqlparse-0.4.4 typing-extensions-4.8.0
$ cd mysite
$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying users.0001_initial... OK
  Applying contenttypes.0001_initial... OK
...
  Applying sessions.0001_initial... OK
$ python3 manage.py createsuperuser
Email address: admin@example.com
Name: admin
Password: 
...
Superuser created successfully.
$ python3 manage.py runserver
```

inspired by ["Customizing authentication in Django"](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/)
