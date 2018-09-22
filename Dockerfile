# Use an official Python runtime as a parent image
FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /uocudg
ADD requirements.txt /uocudg/
RUN pip install -r requirements.txt
ADD . /uocudg/
#RUN python uocudg/manage.py makemigrations
#RUN python uocudg/manage.py migrate