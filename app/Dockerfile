FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR app

ENV POSTGRES_USER=postgres \
      POSTGRES_DB=user_management \
      POSTGRES_PASSWORD=password \
      POSTGRES_HOST=db