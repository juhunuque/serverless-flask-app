FROM python:3.7.1

ENV FLASK_APP "src/api/handler.py"
ENV FLASK_ENV "development"
ENV DEBUG "True"
ENV DYNAMO_CLIENTS_TABLE "bank_users_dev"
ENV AWS_REGION "us-east-1"
ENV IS_OFFLINE "True"
ENV DYNAMO_LOCAL_URL "http://db:8000"
ENV FLASK_DEBUG 1
ENV AWS_ACCESS_KEY_ID "AWS_ACCESS_KEY_ID"
ENV AWS_SECRET_ACCESS_KEY "AWS_SECRET_ACCESS_KEY"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000
CMD python -m flask run --host=0.0.0.0