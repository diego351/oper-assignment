# Oper assignment

1. install latest python (3.11), clone repository, change directory to it `cd quiz-oper-assignment`
2. create new virtualenv `python3 -m venv .venv`
3. activate virtualenv `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. change directory to the quiz directory `cd quiz`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8. `python manage.py test`
9. `python manage.py runserver`
10. enter `127.0.0.1:8000/admin` via browser, login, create token, copy it
11. enter `127.0.0.1:8000/docs` via browser to see api docs and interact with it. Paste it to Authorisation header on the right in a format `"Token <your token>"`. Most likely this you can work with the interactive API exclusively. Excuse my UUIDs, we don't want anybody to iterate easly over our API :)

## The general flow:

1. Create new quiz either via API with `POST /api/quizes` or from admin. `Remember quiz_id`
2. Send invitation to the quiz with: `POST /api/quizes/{quiz_id}/invite`. Check the console to see email. Remember token.
3. Use token to authorise. Rember about 'Token ' prefix.
4. Accept the invitation with `POST /api/quizes/{id}/accept` passing `quiz_id`. You will get `user_quiz_id` in return. This is new identifier other than quiz_id. Remember it.
5. You can retrive the quiz content with `GET /api/user_quizes/{id}` passing `user_quiz_id`
6. You can post your answers with `POST /api/user_quizes/{id}/answers` also using `user_quiz_id`.
7. You can list all your quizes with `GET /api/quizes`. From participator side you will get your all active quizes that you accepted before and didn't finish. From creator side you see all your quiz history you previously created.

## Imporant

The project has been developed as quick as possible, due to strict time constraints, so no DDD, purely djangoish way. I wanted to develop as much functionalities as possible, very little tests.

TODO:

more tests

add browsing viewsets

progress of the quiz

check results via api

notify about results
