FROM python:3

WORKDIR /python
RUN apt-get update
RUN apt-get install -y build-essential
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python"]
