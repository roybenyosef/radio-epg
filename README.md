# Radio EPG

Good examples:
* https://github.com/aws-samples/aws-cdk-examples/blob/master/python/lambda-cron/app.py
* https://docs.aws.amazon.com/code-samples/latest/catalog/welcome.html

### AWS setup
* Install aws cli: https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html
  * pip install awscli
* configure aws cli: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
  * create admin user, create group use access key and secret in 'aws configure' command

### CDK 
see: https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
* use python 3.7! there's a bug https://github.com/aws/aws-cdk/issues/4699
* install nodejs (add to path)
* install cdk: 'npm install -g aws-cdk'
* init the project: cdk init --language python
* install pipenv: pip install pipenv
* run pipenv install
* pipenv shell

### CDK Notes

# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


## In the CDK project
* 
* install boto3: pipenv install boto3
* pipenv didn't work well, installed with pip: aws_s3, aws_lambda
* pip install aws_cdk.aws_apigateway aws_cdk.aws_lambda aws_cdk.aws_s3
* pip install aws-cdk.aws-events-targets
* implement function according to: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/lambda-cron/app.py
* kill env: cdk destroy

