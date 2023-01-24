#!/usr/bin/env python3

import aws_cdk as cdk

from feed_cabinet_4.feed_cabinet_4_stack import FeedCabinet4Stack


app = cdk.App()
FeedCabinet4Stack(app, "feed-cabinet-4")

app.synth()
