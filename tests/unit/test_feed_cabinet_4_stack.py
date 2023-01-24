import aws_cdk as core
import aws_cdk.assertions as assertions
from feed_cabinet_4.feed_cabinet_4_stack import FeedCabinet4Stack


def test_sqs_queue_created():
    app = core.App()
    stack = FeedCabinet4Stack(app, "feed-cabinet-4")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = FeedCabinet4Stack(app, "feed-cabinet-4")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
