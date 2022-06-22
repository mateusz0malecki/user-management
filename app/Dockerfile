FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR app

ENV POSTGRES_USER=postgres \
      POSTGRES_DB=user_management \
      POSTGRES_PASSWORD=password \
      POSTGRES_HOST=db \
      SECRET_KEY=cb6bc018305120bca8c8d9241d3c2cc7271bd99465736bbd871ffb2c98b776ac \
      ALGORITHM=HS256
