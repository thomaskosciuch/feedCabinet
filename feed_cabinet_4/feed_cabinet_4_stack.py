from constructs import Construct
from aws_cdk import (
    Stack,
    BundlingOptions,
    aws_events_targets,
    aws_events,
    aws_lambda,
    aws_ssm,
)

NAME = 'FeedCabinet'

class FeedCabinet4Stack(Stack):

    def cron(self, aws_events, cycle) -> aws_events:
        return aws_events.Rule(
            self, "Rule",
            schedule=cycle,
        )

    def get_env_vars(self, ) -> dict:
        access_key = aws_ssm.StringParameter.value_for_string_parameter(
            self, "synthetic_holding_aws_access_key_id")
        secret_access_key = aws_ssm.StringParameter.value_for_string_parameter(
            self, "synthetic_holding_secret_access_key")
        sentry_dsn = aws_ssm.StringParameter.value_for_string_parameter(
            self, "LAMBDA_SENTRY_DSN")
        return {
            "KEY_ID": access_key, 
            "ACCESS_KEY": secret_access_key,
            "NAME": NAME,
            "SENTRY_DSN": sentry_dsn
        }

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
            environment= self.get_env_vars(),
            handler='hello.handler',
        )

        # runs at 4 UTC every weekday.
        rule = self.cron(aws_events, aws_events.Schedule.cron(
                minute='0',
                hour='4',
                month='*',
                week_day='MON-FRI',
                year='*')
            ,)
        rule.add_target(aws_events_targets.LambdaFunction(lambda_function))
