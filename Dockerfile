 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements1.txt /code/
 ADD requirements2.txt /code/
 RUN pip install -r requirements1.txt
 RUN pip install -r requirements2.txt
 ADD . /code/