from sentry import init_sentry
from sentry_sdk import add_breadcrumb, capture_message

def handler(event, context):
    init_sentry()
    a = capture_message(message='testing sentry in lambda')


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'thank you please: {a}'
    }
