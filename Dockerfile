# Use an official Python runtime as a parent image
FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /uocsecrets
WORKDIR /uocsecrets
ADD requirements.txt /uocsecrets
RUN pip install -r requirements.txt
ADD . /uocsecrets
#RUN python uocudg/manage.py makemigrations
#RUN python uocudg/manage.py migrate