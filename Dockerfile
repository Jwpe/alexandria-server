FROM python:3.5

ADD requirements.txt /code/

WORKDIR /code/

RUN pip install -r requirements.txt

ADD . /code/

CMD python manage.py runserver 0.0.0.0:8000