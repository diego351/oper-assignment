1. install latest python (3.11)
2. create new virtualenv python3 -m venv .venv
3. activate virtualenv source .venv/bin/activate
4. change directory to the quiz directory cd quiz-oper-assignment/quiz
5. pip install -r ../requirements.txt
6. python manage.py migrate
7. python manage.py createsuperuser
8. python manage.py runserver
9. enter 127.0.0.1:8000/admin via browser

todo:

repo gitowe

api:

twórca:
widzi i zarządza tylko swoimi quizami
tworzenie quizu
zapraszanie uczestników do quizu
sprawdzanie progresu quizu
sprawdzanie wyniku quizu
wysyłanie wyniku quizu mailem
przeglądanie quizów, uczestników, zaproszeń, odpowiedzi, filtrowanie, wyszukiwanie

quizer:
widzi tylko swoje quizy
wystartowanie quizu
paginowana lista pytań + mozliwych odpowiedzi
zupdatowanie odpowiedzi na konkretne pytanie

manualne zakończenie quizu, automatyczne zakończenie quizu
celery task po upływie limitu czasu, chyba ze ktos manualnie zakonczyl wczesniej.
usuwać taska czy w tasku pomijać, jezeli juz wysłano

dokumentacja api:

testy:

admin:
generowanie CSV z dziennym raportem aplikacji
