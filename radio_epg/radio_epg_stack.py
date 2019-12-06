from aws_cdk import (
    core,
    aws_events as events,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subs
)
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.core import Duration


class RadioEpgStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        data_bucket_lifecycle_rules = s3.LifecycleRule(noncurrent_version_expiration=Duration.days(3))
        epg_data_s3_bucket_name = 'epg-data-s3-bucket-42'
        epg_data_s3_bucket = s3.Bucket(self,
                                       'EpgDataBucket',
                                       bucket_name=epg_data_s3_bucket_name,
                                       versioned=True,
                                       lifecycle_rules=[data_bucket_lifecycle_rules],
                                       removal_policy=core.RemovalPolicy.DESTROY,
                                       block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        epg_out_s3_bucket_name = 'epg-out-s3-bucket-42'
        epg_out_s3_bucket = s3.Bucket(self,
                                      'EpgOutBucket',
                                      bucket_name=epg_out_s3_bucket_name,
                                      versioned=False,
                                      public_read_access=True,
                                      removal_policy=core.RemovalPolicy.DESTROY)


        topic = sns.Topic(scope=self, id="epg-update-fn-errors-topic",
                          display_name="epg data current show updater errors topic")

        topic.add_subscription(subs.EmailSubscription("roy.benyosef@gmail.com"))
        snsAction = SnsAction(topic)

        with open("show_updater_handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambda_name = 'epg_data_current_show_updater'
        lambda_fn = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment=dict(DATA_BUCKET_NAME=epg_data_s3_bucket.bucket_name,
                             OUT_BUCKET_NAME=epg_out_s3_bucket.bucket_name)
        )

        epg_data_s3_bucket.grant_read(lambda_fn.role)
        epg_out_s3_bucket.grant_read_write(lambda_fn.role)

        # Run every 5 minutes
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(5))
        )
        rule.add_target(targets.LambdaFunction(lambda_fn))

        error_alarm = lambda_fn.metric_all_errors().create_alarm(self, "fn-error-alarm",
                                                                 threshold=1,
                                                                 alarm_name="epg-data-update-alarm",
                                                                 evaluation_periods=1,
                                                                 period=Duration.minutes(5))

        snsAction.bind(self, error_alarm)

        #error_alarm.add_alarm_action()
        #error_alarm.add_alarm_action(self, topic)
        #error_alarm.add_alarm_action(topic)
        #cloudwatch.Alarm.add_alarm_action(error_alarm)
