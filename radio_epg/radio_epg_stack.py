from aws_cdk import (
    core,
    aws_events as events,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events_targets as targets,)


class RadioEpgStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        epg_data_s3_bucket = s3.Bucket(self,
                                       'Bucket',
                                       versioned=True,
                                       removal_policy=core.RemovalPolicy.DESTROY)
                                       #block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        with open("show_updater_handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambda_name = 'epg_data_current_show_updater'
        lambda_fn = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment=dict(BUCKET_NAME=epg_data_s3_bucket.bucket_name)
        )

        epg_data_s3_bucket.grant_read(lambda_fn)

        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0/1',
                hour='*',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambda_fn))
