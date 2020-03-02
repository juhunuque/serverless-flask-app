#!/bin/sh
export AWS_NODEJS_CONNECTION_REUSE_ENABLED=1
export DEBUG="False"
export TESTING="True"
export WTF_CSRF_ENABLED="False"
export DYNAMO_CLIENTS_TABLE="bank_users_test"
export AWS_REGION="us-east-1"
export IS_OFFLINE="True"
export DYNAMO_LOCAL_URL="http://0.0.0.0:8000"

python -m unittest discover -s tests -t src
