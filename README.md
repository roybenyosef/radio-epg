# Radio EPG

##Getting started:

### AWS setup
* Install aws cli: https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html
  * pip install awscli
* configure aws cli: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
  * create admin user, create group use access key and secret in 'aws configure' command
* test awscli with 'aws -v'

### Python
* install python 3.7 (cdk has a bug with 3.8: https://github.com/aws/aws-cdk/issues/4699)
* update pip: 'pip install --upgrade pip'

### CDK 
see: https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
* use python 3.7! there's a bug https://github.com/aws/aws-cdk/issues/4699
* install nodejs (add to path)
* install cdk: 'npm install -g aws-cdk'
* init the project: cdk init --language python

### Installing third-party dependencies
cdk does NOT install the third party dependencies you may have.
use this: https://gitlab.com/josef.stach/aws-cdk-lambda-asset/

### EPG project
* clone this repo ('git clonse https://github.com/roybenyosef/radio-epg.git')
* create an activate your python virtual env however you like to. under windows you can do this:
  * python -m venv .venv
  * run '.venv\scripts\activate' (run deactivate to exit the venv)
* install all dependencies with: 'pip install -r requirements.txt'
* check that everything is ok by running 'cdk synth' which will synthesize your expected Cloudformation yaml
* start hacking!
* Note: kill your env with 'cdk destroy'

### CDK Notes (From initializing a project with cdk)

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


## Useful links:
* https://github.com/aws-samples/aws-cdk-examples/blob/master/python/lambda-cron/app.py
* https://docs.aws.amazon.com/code-samples/latest/catalog/welcome.html
* https://blog.codecentric.de/en/2019/10/aws-cdk-part-2-s3-bucket/
* aws libraries docs: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.core/Duration.html
* implement function according to: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/lambda-cron/app.py

## CloudFront
we use cloudFront to deliver the administrator web app, which is a simple static website that allows the user to get and update the epg json. 
see https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-s3-amazon-cloudfront-a-match-made-in-the-cloud/
to serve your s3 stored static web site.<BR>
In case you are seeing your update site, it is because cf uses cache for performance. you need to invalidate files.
see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html

### Also see:
* https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-enable-cognito-user-pool.html
* https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-invoke-api-integrated-with-cognito-user-pool.html
