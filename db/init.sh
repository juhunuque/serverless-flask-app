#!/bin/sh

echo "Creating table \n"
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID \
AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY \
aws dynamodb create-table \
	--cli-input-json "$(cat create-table.json)" \
	--endpoint-url http://db:8000 \
	--region us-east-1

echo "List tables \n"
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID \
AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY \
aws dynamodb list-tables \
	--endpoint-url http://db:8000 \
	--region us-east-1

