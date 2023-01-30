from constructs import Construct
from aws_cdk import (
    Stack,
    BundlingOptions,
    Duration,
    aws_events_targets,
    aws_events,
    aws_lambda,
    aws_cloudwatch
)
from feed_cabinet_4.env_vars import get_env_vars

NAME = 'FeedCabinet'

class FeedCabinet4Stack(Stack):

    def cron(self, aws_events, cycle) -> aws_events:
        return aws_events.Rule(
            self, "Rule",
            schedule=cycle,
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = aws_lambda.Function(
            self, 
            NAME,
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code =aws_lambda.Code.from_asset(
                "lambda",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ],
                )
            ),
            timeout=Duration.minutes(10),
            environment=get_env_vars(self, NAME),
            handler='main.handler'
            )

        if lambda_function.timeout:
            aws_cloudwatch.Alarm(self, f"{NAME} max duration / timeout",
                metric=lambda_function.metric_duration(),
                evaluation_periods=1,
                datapoints_to_alarm=1,
                threshold=lambda_function.timeout.to_milliseconds(),
                treat_missing_data=aws_cloudwatch.TreatMissingData.IGNORE,
                alarm_name="{NAME} max duration / timeout"
            )

        # runs at 4 UTC every weekday.
        rule = self.cron(aws_events, aws_events.Schedule.cron(
            minute='0', hour='4', month='*', week_day='MON-FRI', year='*'),)

        event = {
            "folder_name": "/users/ETFCM/RPT",
            "bucket_name": "qnext.custodian.nbin"
        }
        rule.add_target(aws_events_targets.LambdaFunction(lambda_function, retry_attempts=10))
