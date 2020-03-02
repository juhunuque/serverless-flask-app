# User management microservice

Python-serverless project created using serverless framework on top of a flask layer. It can be deployed as lambdas or a flask service.

# Architectural viewpoints

This section will elaborate on the architectural decisions, using the model of viewpoints.

## Functional viewpoint

The functional requirements are simple: allow a user to complete the onboards process, query his card's pin and change his password in case needed.
Below a functional representation of the components involved.

![Alt text](static/functional_diagram.png?raw=true "Functional diagram")

## Information viewpoint

All about the data management.
The database implemented on this project was Dynamodb for a very simple reasoning process:

* No complex relations.
* No transactions required.
* Leverage AWS tools (Do not reinvent the wheel).
* And finally but no less important: keep it simple :wink:


For the current version, only one document was created called "user".

## Deployment viewpoint

A nice to have was to implement a CI/CD process. Continue with the principle of reuse AWS products, were implemented CodePipeline, CodeCommit and CodeBuild.
Following a Git-flow branching, every code pushed into "master" is deployed, relying on Serverless framework to accomplish this. Below a diagram of how it works

![Alt text](static/reference_deployment.png?raw=true "Deployment diagram")

Also, this project is powered by LocalStack. This means we can try the deployment in a AWS instance locally. Below are the steps to use this.

## Development viewpoint
Section to elaborate about the project structure, philosophy, trade-offs, etc.

* The project was developed following the principles of atomicity and generalization: every method has its specific purpose and can be reused in different flows.
* It was required to be developed using Python and be prepared to be deployed as AWS lambdas.
* To ease the process of local development and deploy, Serverless framework was incorporated into the project.
* The project was developed using layers design, not only layers for the code, also for the infrastructure, allowing us to decompose the project and reuse only what is needed (We should always point to modularize our software to either recycle later or to make enhancements quicker without broke any part).
* The project was build using 3 layers design and DDD (Domain Driven Design). First layers catch the user requests and redirect them to the proper resolver. All the business logic was incapsulated in services. And finally the data layer. There is no ORM included for the sake of speed the delivery, however since it's a layer, it can be easily replaced to support a easier implementation.
* DDD was mentioned before. All the business logic is included in the domain service file, that uses little pieces from the application services to build a flow.
* Even the architecture has layers. On the top it's used serverless to handle the lambdas part. But behind that layer we found a Flask service. It can be deployed as it's needed, either using lambdas or using a container (ECS or even EKS).
* For encrypting the sensible data state in the requirements, there is a **layer** in charge of this. Currently is a very basic implementation, however, it can be easily improved without break any other part.
* Tests are a very important part of every software. It was included unit and integration tests, in charge of testing the specific parts and the whole flows.
* LocalStack was also included for testing the deployment process

# The project
## Requirements
- NodeJs > 12
- npm
- Python > 3.5
- pip
- Docker
- docker-compose
- serverless (npm)
- virtualenv (pip)
- JRE > 8 (If you are planning to use serverless-dynamodb-local)

## Start using the app right away
For the sake of convenience, all the steps were included in a Makefile. Below the steps to use it.
Note: Building the main docker might take a while. Use this time to grab a drink :beer:

* Execute right away
```shell script
make init
```

* Stop everything
```shell script
make stop
```


## Local development
### Local database
A serverless plugin was included to start up a local instance of dynamodb.
Prior run the app you must run the database.

Install serverless plugins:
```shell script
npm install
sls dynamodb install
```

```
sls dynamodb start -s dev
```

Note: Do not forget to include the --stage (-s) flag. 
This is necessary to extract the environment variables from the correct file.

### Virtual environment
It's always a good practice to isolate the environment requirements.
To develop locally, create a virtual environment and install your dependencies:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, run your app:
```
sls wsgi serve -s dev
```

Navigate to [localhost:5000/](http://localhost:5000) to see your app running locally.


## Tests

### Run tests manually
The integration tests rely on the use of a database instance. 
For this purpose, run the dynamodb locally prior to run the tests.

```shell script
sls dynamodb start -s test
```

For easing the process, you can execute the tests using a shell script created for this purpose.
```shell script
./run_tests.sh
```

## Deployment
### Manual deploy
You must have your credentials already configured in your local aws credentials store.

```
$ npm install -g serverless
$ serverless deploy
```

### Local deployment using LocalStack
The project includes LocalStack, which mocks AWS services to have them running in local environment. 
You must have configured the local environment with the project (python requirements and node modules installed).

Then, firstable you must have LocalStack running (it takes a while, when it's done, there shall be an output with the label Ready).
```shell script
docker-compose -f localstack-compose.yml up -d
```

When the LocalStack is ready, trigger the local deploy:
```shell script
sls deploy -s local -v
```

The stage must be local in order to get it work. Then you will see the exact same output as it would be deployed in AWS.

### CI/CD: Using AWS magic
AWS offers a couple of tools we can use to automate the continuous deployment.
You can see a file called "buildspec.yml" which is read by CodeBuild/CodePipeline to perform the deployment.


# Endpoints summary

* User’s onboarding, 

User's onboarding. Assign the PIN to the card and store their password and PIN.

POST - /user/register

headers:
```
"Content-Type": "application/json"
```
body
```json
{
	"email": "test@mail.com",
	"password": "12345",
	"pin": "3412"
}
```

* Retrieve the card's pin
They should be able to retrieve their unencrypted PIN at any moment, must be authenticated.

GET - /user/retrievePin

headers:
```
"Content-Type": "application/json"
```
Authorization:
Use the credentials of a user already registered into the app.
```
Basic auth
```

* Change password
The user should be able to change their password without losing access to their PIN

PUT - /user/changePassword

headers:
```
"Content-Type": "application/json"
```
body
```
{
	"email": "test@mail.com",
	"oldPassword": "12345",
	"newPassword": "3412"
}
```