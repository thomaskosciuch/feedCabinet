from sentry_sdk import add_breadcrumb, capture_message

from sentry import init_sentry
from sftp_connect import sftp_connect


cognitoPublicKey = "https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json"


def handler(event, context):
    init_sentry()
    a = capture_message(message='testing sentry in lambda')
    sftp = sftp_connect()

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'thank you please: {a} - sftp'
    }
