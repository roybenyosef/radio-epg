from aws_cdk import (
    core,
    aws_events as events,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_cloudwatch as cloudwatch
)
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.core import Duration


class Config:
    # Data bucket settings
    data_bucket_name = 'epg-data-s3-bucket-42'
    data_bucket_noncurrent_version_expiration = Duration.days(30)

    # Out bucket settings
    out_bucket_name = 'epg-out-s3-bucket-42'

    # Notifications
    email_recipient = 'trickster79@gmail.com'

    # Update function
    update_function_rate = Duration.minutes(5)
    error_count_to_notify = 12

    @staticmethod
    def period_to_check_error_count() -> Duration:
        return Duration.minutes(Config.update_function_rate.to_minutes() * Config.error_count_to_notify * 2)


class RadioEpgStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Buckets
        data_bucket_lifecycle_rules = s3.LifecycleRule(noncurrent_version_expiration=Config.data_bucket_noncurrent_version_expiration)
        epg_data_s3_bucket_name = Config.data_bucket_name
        epg_data_s3_bucket = s3.Bucket(self,
                                       'EpgDataBucket',
                                       bucket_name=epg_data_s3_bucket_name,
                                       versioned=True,
                                       lifecycle_rules=[data_bucket_lifecycle_rules],
                                       removal_policy=core.RemovalPolicy.RETAIN,
                                       block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        epg_out_s3_bucket_name = Config.out_bucket_name
        epg_out_s3_bucket = s3.Bucket(self,
                                      'EpgOutBucket',
                                      bucket_name=epg_out_s3_bucket_name,
                                      versioned=False,
                                      public_read_access=True,
                                      removal_policy=core.RemovalPolicy.RETAIN)

        # Create Lambda functions
        with open("show_updater_handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambda_fn = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment=dict(DATA_BUCKET_NAME=epg_data_s3_bucket.bucket_name,
                             OUT_BUCKET_NAME=epg_out_s3_bucket.bucket_name)
        )

        # Grant permissions on buckets
        epg_data_s3_bucket.grant_read(lambda_fn.role)
        epg_out_s3_bucket.grant_read_write(lambda_fn.role)

        # Run lambda every X minutes
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Config.update_function_rate)
        )
        rule.add_target(targets.LambdaFunction(lambda_fn))

        # Create SNS Topic
        fn_error_topic = sns.Topic(scope=self, id="epg-update-fn-errors-topic",
                                   display_name="Radio epg current show function errors topic")

        fn_error_topic.add_subscription(subs.EmailSubscription(Config.email_recipient))

        # Create function error alarm
        fn_error_alarm = lambda_fn.metric_all_errors().create_alarm(self, "fn-error-alarm",
                                                                    threshold=Config.error_count_to_notify,
                                                                    alarm_name="epg-data-update-alarm",
                                                                    evaluation_periods=1,
                                                                    period=Config.period_to_check_error_count())

        fn_error_alarm.add_alarm_action(SnsAction(fn_error_topic))




