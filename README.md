# Oper assignment

1. install latest python (3.11)
2. create new virtualenv `python3 -m venv .venv`
3. activate virtualenv `source .venv/bin/activate`
4. change directory to the quiz directory `cd quiz-oper-assignment/quiz`
5. `pip install -r ../requirements.txt`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8. `python manage.py test`
9. `python manage.py runserver`
10. enter 127.0.0.1:8000/admin via browser, login, create token, copy it
11. enter 127.0.0.1:8000/docs via browser to see api docs and interactively interact with it. Paste it to Authorisation header on the right in a format `"Token <your token>"`

todo:
more tests

add browsing viewsets

progress of the quiz

check results via api

notify about results
