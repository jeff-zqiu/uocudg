# Use an official Python runtime as a parent image
FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /uocweb
WORKDIR /uocweb
ADD requirements.txt /uocweb
RUN pip install -r requirements.txt
ADD . /uocweb
#RUN python uocudg/manage.py makemigrations
#RUN python uocudg/manage.py migrate