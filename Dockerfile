# Use an official Python runtime as a parent image
FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR .
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
#RUN python uocudg/manage.py makemigrations
#RUN python uocudg/manage.py migrate